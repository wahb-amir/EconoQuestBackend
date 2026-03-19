import type { FastifyInstance, FastifyRequest } from "fastify";
import type { RawData } from "ws";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import { hashState } from "../services/Statehash.js";
import { getCachedHint, setCachedHint } from "../services/cache.js";
import {
  getFreeSpace,
  markBusy,
  markFree,
  enqueue,
  processQueue,
} from "../services/queue.js";
import { config } from "../config.js";

// ── Lazy Supabase client ──────────────────────────────────────────────────────

let _supabase: SupabaseClient | null = null;

function getSupabase(): SupabaseClient {
  if (!_supabase) {
    if (!process.env.SUPABASE_URL || !process.env.SUPABASE_SERVICE_KEY) {
      throw new Error("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY");
    }
    _supabase = createClient(
      process.env.SUPABASE_URL,
      process.env.SUPABASE_SERVICE_KEY,
    );
  }
  return _supabase;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function parseCookies(header: string): Record<string, string> {
  return Object.fromEntries(
    header.split(";").map((c) => {
      const [k, ...v] = c.trim().split("=");
      return [k.trim(), v.join("=")];
    }),
  );
}

function send(socket: any, data: unknown): void {
  if (socket.readyState === 1) {
    socket.send(JSON.stringify(data));
  }
}

function rawToString(raw: RawData): string {
  if (Buffer.isBuffer(raw)) return raw.toString("utf8");
  if (Array.isArray(raw)) return Buffer.concat(raw).toString("utf8");
  return Buffer.from(raw as ArrayBuffer).toString("utf8");
}

// ── Stream hint from HF Space → client ───────────────────────────────────────

async function streamHintToClient(
  spaceUrl: string,
  body: unknown,
  socket: any,
): Promise<string> {
  const response = await fetch(`${spaceUrl}/hint-stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${config.internalToken}`,
      Accept: "text/event-stream",
    },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(30_000),
  });

  if (!response.ok) {
    throw new Error(`Hint space returned ${response.status}`);
  }

  const reader = response.body!.getReader();
  const decoder = new TextDecoder();
  let fullHint = "";
  let buffer = "";

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
        if (parsed.type === "meta") {
          send(socket, {
            type: "meta",
            conflicts: parsed.conflicts ?? [],
            chunks: parsed.chunks_used ?? [],
          });
        }
        if (parsed.type === "token") {
          fullHint += parsed.text;
          send(socket, { type: "token", text: parsed.text });
        }
        if (parsed.type === "done") {
          send(socket, { type: "done" });
        }
      } catch {
        // malformed SSE chunk — skip
      }
    }
  }

  return fullHint;
}

// ── Stream cached hint word by word ──────────────────────────────────────────

async function streamCachedHint(hint: string, socket: any): Promise<void> {
  const words = hint.split(" ");
  for (const word of words) {
    if (socket.readyState !== 1) break;
    send(socket, { type: "token", text: word + " " });
    await new Promise((r) => setTimeout(r, 35));
  }
  send(socket, { type: "done" });
}

// ── WebSocket route ───────────────────────────────────────────────────────────

export async function wsHintRoutes(app: FastifyInstance) {
  await app.register(import("@fastify/websocket"));

  app.get(
    "/ws/hint",
    { websocket: true },
    async (connection: any, req: FastifyRequest) => {
      // @fastify/websocket v8 — raw socket is at connection.socket
      const socket = connection.socket ?? connection;

      // ── Ping keepalive — HF proxy drops idle WS after ~30s ───────────────
      const pingInterval = setInterval(() => {
        if (socket.readyState === 1) {
          socket.ping();
        } else {
          clearInterval(pingInterval);
        }
      }, 20_000);

      send(socket, { type: "connected" });

      socket.on("message", async (raw: RawData) => {
        const text = rawToString(raw).trim();

        // ignore empty messages
        if (!text) return;

        // handle client ping
        try {
          const peek = JSON.parse(text);
          if (peek?.type === "ping") {
            send(socket, { type: "pong" });
            return;
          }
        } catch {
          // not a ping — continue
        }

        console.log("[ws/hint] received:", text.substring(0, 120));

        // 1. Parse state
        let msg: any;
        let state: Record<string, unknown>;
        try {
          msg = JSON.parse(text);
          state = msg.state;
          if (!state || typeof state !== "object") 
            throw new Error("Missing state");
        } catch (e: any) {
          console.error("[ws/hint] parse error:", e.message);
          send(socket, { type: "error", message: "Invalid message format" });
          return;
        }

        // 2. Verify JWT from cookie

        const cookieHeader = req.headers.cookie ?? "";
        const cookies = parseCookies(cookieHeader);

        // token can come from cookie (same-domain) or message payload (cross-domain)
        const accessToken =
          cookies["access_token"] || ((msg as any).token as string);

        if (!accessToken) {
          send(socket, {
            type: "error",
            message: "Unauthorized — please sign in",
          });
          return;
        }

        let userId: string;
        try {
          const { data, error } = await getSupabase().auth.getUser(accessToken);
          if (error || !data.user) throw new Error("Invalid token");
          userId = data.user.id;
        } catch {
          send(socket, {
            type: "error",
            message: "Session expired — please sign in again",
          });
          return;
        }

        // 3. Hash state → check LRU cache
        const cacheKey = hashState(state);
        const cached = await getCachedHint(cacheKey);

        if (cached) {
          send(socket, { type: "cache_hit" });
          await streamCachedHint(cached, socket);
          return;
        }

        const requestBody = { state };

        // 4. Pick free Space or queue
        const freeSpace = getFreeSpace();

        if (freeSpace) {
          markBusy(freeSpace.id);
          send(socket, { type: "processing" });

          try {
            const fullHint = await streamHintToClient(
              freeSpace.url,
              requestBody,
              socket,
            );
            setCachedHint(cacheKey, fullHint, state).catch(() => {});
          } catch (err: any) {
            console.error("[ws/hint] stream error:", err.message);
            send(socket, {
              type: "error",
              message: `Advisor error: ${err.message ?? "Unknown"}`,
            });
          } finally {
            markFree(freeSpace.id);
            processQueue();
          }
        } else {
          // both Spaces busy — queue
          await new Promise<void>((resolve) => {
            const position = enqueue({
              ws: socket,
              body: requestBody,
              cacheKey,
              userId,
              resolve,
            });
            send(socket, { type: "queued", position });
          });

          const nowFree = getFreeSpace();
          if (nowFree && socket.readyState === 1) {
            markBusy(nowFree.id);
            send(socket, { type: "processing" });

            try {
              const fullHint = await streamHintToClient(
                nowFree.url,
                requestBody,
                socket,
              );
              setCachedHint(cacheKey, fullHint, state).catch(() => {});
            } catch (err: any) {
              send(socket, {
                type: "error",
                message: `Advisor error: ${err.message ?? "Unknown"}`,
              });
            } finally {
              markFree(nowFree.id);
              processQueue();
            }
          }
        }
      });

      socket.on("close", () => {
        clearInterval(pingInterval);
        console.log("[ws/hint] client disconnected");
      });

      socket.on("error", (err: Error) => {
        clearInterval(pingInterval);
        console.error("[ws/hint] socket error:", err.message);
      });
    },
  );
}
