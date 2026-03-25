import type { FastifyInstance } from "fastify";
import { markFree, processQueue, getQueueStatus } from "../services/queue.js";
import { config } from "../config.js";

export async function internalRoutes(app: FastifyInstance) {
  // called by HF Space when it finishes processing a request
  app.post("/internal/space-free", async (request, reply) => {
    const auth = request.headers.authorization;
    if (auth !== `Bearer ${config.internalToken}`) {
      return reply.status(401).send({ error: "Unauthorized" });
    }

    const { space_id } = request.body as { space_id?: string };
    if (!space_id) {
      return reply.status(400).send({ error: "Missing space_id" });
    }

    markFree(space_id);
    processQueue();

    const status = getQueueStatus();
    console.log(
      `[internal] ${space_id} marked free — queue: ${status.queueLength}`,
    );

    return reply.send({ ok: true, queue: status.queueLength });
  });

  // queue + space health status (internal debug)
  app.get("/internal/queue-status", async (request, reply) => {
    const auth = request.headers.authorization;
    if (auth !== `Bearer ${config.internalToken}`) {
      return reply.status(401).send({ error: "Unauthorized" });
    }
    return reply.send(getQueueStatus());
  });
}
