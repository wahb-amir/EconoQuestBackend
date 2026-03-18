import type { FastifyInstance } from "fastify";
import { getPoolStatus } from "../services/loadBalancer.js";

export async function statusRoutes(app: FastifyInstance) {
  app.get("/health", async () => ({
    status: "ok",
    service: "proxy"
  }));

  app.get("/api/status", async () => ({
    status: "ok",
    pool: getPoolStatus(),
    timestamp: new Date().toISOString(),
  }));
}