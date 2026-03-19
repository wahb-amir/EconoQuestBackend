import type { FastifyInstance } from "fastify";
import WebSocket from "ws";
import { createClient, SupabaseClient } from "@supabase/supabase-js";
import { hashState } from "../services/Statehash.js";
import { getCachedHint, setCachedHint } from "../services/cache.js";
import {
  getFreeSpace,
  markBusy,
  markFree,
  enqueue,
  processQueue,
} from '../services/queue.js'
import { config } from "../config.js";

let _supabase: SupabaseClient | null = null;

function getSupabase(): SupabaseClient {
  if (!_supabase) {
    if (!process.env.SUPABASE_URL || !process.env.SUPABASE_SERVICE_KEY) {
      throw new Error("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY");
    }
    _supabase = createClient(
      process.env.SUPABASE_URL,
      process.env.SUPABASE_SERVICE_KEY
    );
  }
  return _supabase;
}

// ── Parse cookie header into key/value map ────────────────────────────────────

function parseCookies(header: string): Record<string, string> {
  return Object.fromEntries(
    header.split(";").map(c => {
      const [k, ...v] = c.trim().split("=");
      return [k.trim(), v.join("=")];
    })
  );
}

// ── Stream hint from HF Space → WebSocket client ──────────────────────────────

async function streamHintToClient(
  spaceUrl: string,
  body:     unknown,
  ws:       WebSocket
): Promise<string> {
  const response = await fetch(`${spaceUrl}/hint-stream`, {
    method:  "POST",
    headers: {
      "Content-Type":  "application/json",
      "Authorization": `Bearer ${config.internalToken}`,
      "Accept":        "text/event-stream",
    },
    body:   JSON.stringify(body),
    signal: AbortSignal.timeout(30_000),
  });

  if (!response.ok) {
    throw new Error(`Hint space returned ${response.status}`);
  }

  const reader  = response.body!.getReader();
  const decoder = new TextDecoder();
  let fullHint  = "";
  let buffer    = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      try {
        const parsed = JSON.parse(line.slice(6));

        if (parsed.type === "meta" && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({
            type:      "meta",
            conflicts: parsed.conflicts ?? [],
            chunks:    parsed.chunks_used ?? [],
          }));
        }

        if (parsed.type === "token" && ws.readyState === WebSocket.OPEN) {
          fullHint += parsed.text;
          ws.send(JSON.stringify({ type: "token", text: parsed.text }));
        }

        if (parsed.type === "done" && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: "done" }));
        }
      } catch {
        // malformed SSE chunk — skip
      }
    }
  }

  return fullHint;
}

// ── Stream cached hint word by word ───────────────────────────────────────────

async function streamCachedHint(hint: string, ws: WebSocket): Promise<void> {
  const words = hint.split(" ");
  for (const word of words) {
    if (ws.readyState !== WebSocket.OPEN) break;
    ws.send(JSON.stringify({ type: "token", text: word + " " }));
    await new Promise(r => setTimeout(r, 35));
  }
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: "done" }));
  }
}

// ── WebSocket route ───────────────────────────────────────────────────────────

export async function wsHintRoutes(app: FastifyInstance) {
  await app.register(import("@fastify/websocket"));

  app.get("/ws/hint", { websocket: true }, async (ws, req) => {

    ws.send(JSON.stringify({ type: "connected" }));

    ws.on("message", async (raw: Buffer) => {

      // ── 1. Parse message ────────────────────────────────────────────────
      let state: Record<string, unknown>;
      try {
        const msg = JSON.parse(raw.toString());
        state = msg.state;
        if (!state || typeof state !== "object") throw new Error("Missing state");
      } catch {
        ws.send(JSON.stringify({ type: "error", message: "Invalid message format" }));
        return;
      }

      // ── 2. Verify JWT from cookie (sent automatically on WS upgrade) ────
      const cookieHeader = req.headers.cookie ?? "";
      const cookies      = parseCookies(cookieHeader);
      const accessToken  = cookies["access_token"];

      if (!accessToken) {
        ws.send(JSON.stringify({ type: "error", message: "Unauthorized — please sign in" }));
        return;
      }

      let userId: string;
      try {
        const { data, error } = await getSupabase().auth.getUser(accessToken);
        if (error || !data.user) throw new Error("Invalid token");
        userId = data.user.id;
      } catch {
        ws.send(JSON.stringify({ type: "error", message: "Session expired — please sign in again" }));
        return;
      }

      // ── 3. Hash state → check LRU cache ─────────────────────────────────
      const cacheKey = hashState(state);
      const cached   = await getCachedHint(cacheKey);

      if (cached) {
        ws.send(JSON.stringify({ type: "cache_hit" }));
        await streamCachedHint(cached, ws);
        return;
      }

      const requestBody = { state };

      // ── 4. Pick free Space or queue ──────────────────────────────────────
      const freeSpace = getFreeSpace();

      if (freeSpace) {
        markBusy(freeSpace.id);
        ws.send(JSON.stringify({ type: "processing" }));

        try {
          const fullHint = await streamHintToClient(freeSpace.url, requestBody, ws);
          setCachedHint(cacheKey, fullHint, state).catch(() => {});
        } catch (err: any) {
          console.error("[ws/hint] stream error:", err.message);
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
              type:    "error",
              message: `Advisor error: ${err.message ?? "Unknown"}`,
            }));
          }
        } finally {
          markFree(freeSpace.id);
          processQueue();
        }

      } else {
        // both Spaces busy — queue
        await new Promise<void>((resolve) => {
          const position = enqueue({ ws, body: requestBody, cacheKey, userId, resolve });
          ws.send(JSON.stringify({ type: "queued", position }));
        });

        // resumed when space-free callback fires
        const nowFree = getFreeSpace();
        if (nowFree && ws.readyState === WebSocket.OPEN) {
          markBusy(nowFree.id);
          ws.send(JSON.stringify({ type: "processing" }));

          try {
            const fullHint = await streamHintToClient(nowFree.url, requestBody, ws);
            setCachedHint(cacheKey, fullHint, state).catch(() => {});
          } catch (err: any) {
            if (ws.readyState === WebSocket.OPEN) {
              ws.send(JSON.stringify({
                type:    "error",
                message: `Advisor error: ${err.message ?? "Unknown"}`,
              }));
            }
          } finally {
            markFree(nowFree.id);
            processQueue();
          }
        }
      }
    });

    ws.on("close", () => console.log("[ws/hint] client disconnected"));
    ws.on("error", (err) => console.error("[ws/hint] socket error:", err.message));
  });
}