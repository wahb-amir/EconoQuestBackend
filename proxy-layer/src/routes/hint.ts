import type { FastifyInstance } from "fastify";
import { forwardToSpace } from "../services/loadBalancer.js";

export async function hintRoutes(app: FastifyInstance) {
  app.post("/api/game/hint", {
    preHandler: [(app as any).authenticate],
  }, async (request, reply) => {
    const { data, spaceUsed } = await forwardToSpace(
      "hint",
      "/hint",
      request.body
    );
    return reply.send(data);
  });
}