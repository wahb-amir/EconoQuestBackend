import type { FastifyInstance, FastifyRequest } from "fastify";
import { createClient } from "@supabase/supabase-js";
import { forwardToSpace } from "../services/loadBalancer.js";

let _supabase: any = null;
function getSupabase() {
  if (!_supabase) {
    _supabase = createClient(
      process.env.SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_KEY!
    );
  }
  return _supabase;
}

// verify Supabase JWT from Authorization header or cookie
async function verifyRequest(request: FastifyRequest): Promise<boolean> {
  try {
    // try Authorization header first
    const authHeader = request.headers.authorization;
    const cookieHeader = request.headers.cookie ?? "";

    const cookies = Object.fromEntries(
      cookieHeader.split(";").map(c => {
        const [k, ...v] = c.trim().split("=");
        return [k.trim(), v.join("=")];
      })
    );

    const token =
      authHeader?.replace("Bearer ", "").trim() ||
      cookies["access_token"] ||
      "";

    if (!token) return false;

    const { data, error } = await getSupabase().auth.getUser(token);
    return !error && !!data.user;
  } catch {
    return false;
  }
}

export async function summaryRoutes(app: FastifyInstance) {

  app.post("/api/game/round-summary", async (request, reply) => {
    const ok = await verifyRequest(request);
    if (!ok) return reply.status(401).send({ error: "Unauthorized" });

    try {
      const { data } = await forwardToSpace("summary", "/round-summary", request.body);
      return reply.send(data);
    } catch (err: any) {
      return reply.status(500).send({ error: err.message });
    }
  });

  app.post("/api/game/final-summary", async (request, reply) => {
    const ok = await verifyRequest(request);
    if (!ok) return reply.status(401).send({ error: "Unauthorized" });

    try {
      const { data } = await forwardToSpace("summary", "/summary", request.body);
      return reply.send(data);
    } catch (err: any) {
      return reply.status(500).send({ error: err.message });
    }
  });
}