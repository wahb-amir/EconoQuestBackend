import cron from "node-cron";
import { config } from "../config.js";

const ALL_SPACES = [
  ...config.spaces.hint,
  ...config.spaces.summary,
  config.spaces.auth,         // ← auth service included
].filter(Boolean);            // remove empty strings if not set

async function pingAll() {
  console.log(`[cron] pinging ${ALL_SPACES.length} spaces...`);

  const results = await Promise.allSettled(
    ALL_SPACES.map(async url => {
      const res = await fetch(`${url}/health`, {
        signal: AbortSignal.timeout(config.cron.timeoutMs),
      });
      return { url, ok: res.ok };
    })
  );

  for (const result of results) {
    if (result.status === "fulfilled") {
      console.log(`[cron] ${result.value.url} → ${result.value.ok ? "✓" : "✗"}`);
    } else {
      console.warn(`[cron] ping failed:`, result.reason);
    }
  }
}

export function startHealthCron() {
  pingAll();
  cron.schedule(config.cron.pingInterval, pingAll);
  console.log("[cron] health cron started — interval: 25min");
}
