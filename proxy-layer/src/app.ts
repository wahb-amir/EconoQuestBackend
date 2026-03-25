import Fastify from "fastify";
import cors from "@fastify/cors";
import rateLimit from "@fastify/rate-limit";
import { config } from "./config.js";
import { startHealthCron } from "./services/healthCron.js";
import { hintRoutes } from "./routes/hint.js";
import { summaryRoutes } from "./routes/summary.js";
import { statusRoutes } from "./routes/status.js";
import { wsHintRoutes } from "./routes/Wshint.js";
import authPlugin from "./plugins/auth.js";
import { internalRoutes } from "./routes/Internal.js";

const app = Fastify({ logger: true });

await app.register(cors, { origin: true });

// ── Rate limiting ─────────────────────────────────────────────────────────────
await app.register(rateLimit, {
  global: true,
  max: 60, // 60 requests per window per IP
  timeWindow: "1 minute",
  keyGenerator: (request) =>
    request.headers["x-forwarded-for"]?.toString().split(",")[0].trim() ??
    request.ip,
  errorResponseBuilder: (_request, context) => ({
    statusCode: 429,
    error: "Too Many Requests",
    message: `Rate limit exceeded. Try again in ${Math.ceil(context.ttl / 1000)}s.`,
  }),
});

// tighter limit on AI hint endpoint specifically
app.addHook("onRoute", (routeOptions) => {
  if (
    routeOptions.url === "/api/game/hint" ||
    routeOptions.url === "/ws/hint"
  ) {
    routeOptions.config = {
      rateLimit: {
        max: 10, // 10 hint requests per minute per IP
        timeWindow: "1 minute",
      },
    };
  }
  if (
    routeOptions.url === "/api/game/round-summary" ||
    routeOptions.url === "/api/game/final-summary"
  ) {
    routeOptions.config = {
      rateLimit: {
        max: 20,
        timeWindow: "1 minute",
      },
    };
  }
});

await app.register(authPlugin);
await app.register(statusRoutes);
await app.register(hintRoutes);
await app.register(summaryRoutes);
await app.register(wsHintRoutes);
await app.register(internalRoutes);

await app.listen({ port: config.port, host: "0.0.0.0" });

startHealthCron();
