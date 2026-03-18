import Fastify from "fastify";
import cors from "@fastify/cors";
import { config } from "./config.js";
import { startHealthCron } from "./services/healthCron.js";
import { hintRoutes } from "./routes/hint.js";
import { summaryRoutes } from "./routes/summary.js";
import { statusRoutes } from "./routes/status.js";
import authPlugin from "./plugins/auth.js";

const app = Fastify({ logger: true });

await app.register(cors, { origin: true });
await app.register(authPlugin);
await app.register(statusRoutes);
await app.register(hintRoutes);
await app.register(summaryRoutes);

await app.listen({ port: config.port, host: "0.0.0.0" });

// start pinging HF Spaces
startHealthCron();