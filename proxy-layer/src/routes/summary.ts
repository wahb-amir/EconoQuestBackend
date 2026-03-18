import type { FastifyInstance } from "fastify";
import { forwardToSpace } from "../services/loadBalancer.js";

export async function summaryRoutes(app: FastifyInstance) {

  // called after each round — fire and forget from frontend
  app.post("/api/game/round-summary", {
    preHandler: [(app as any).authenticate],
  }, async (request, reply) => {
    const { data } = await forwardToSpace(
      "summary",
      "/round-summary",
      request.body
    );
    return reply.send(data);
  });

  // called once at game end — returns full summary
  app.post("/api/game/final-summary", {
    preHandler: [(app as any).authenticate],
  }, async (request, reply) => {
    const { data } = await forwardToSpace(
      "summary",
      "/summary",
      request.body
    );
    return reply.send(data);
  });
}