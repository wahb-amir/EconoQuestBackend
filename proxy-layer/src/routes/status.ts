import type { FastifyInstance } from "fastify";
import { getQueueStatus } from "../services/queue.js";
import { createClient } from "@supabase/supabase-js";

export async function statusRoutes(app: FastifyInstance) {
  app.get("/health", async () => ({
    status: "ok",
    service: "proxy",
  }));

  app.get("/api/status", async () => ({
    status: "ok",
    pool: getQueueStatus(),
    timestamp: new Date().toISOString(),
  }));
}
