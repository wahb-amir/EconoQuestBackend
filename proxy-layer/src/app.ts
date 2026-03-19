import Fastify from "fastify";
import cors from "@fastify/cors";
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
await app.register(authPlugin);
await app.register(statusRoutes);
await app.register(hintRoutes);
await app.register(summaryRoutes);
await app.register(wsHintRoutes);   // WebSocket + queue
await app.register(internalRoutes); // space-free callback

await app.listen({ port: config.port, host: "0.0.0.0" });

startHealthCron();