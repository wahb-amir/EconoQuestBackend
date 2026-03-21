import { config } from "../config.js";

const MAX_CONCURRENT = 10; // max requests per space at once

interface SpaceState {
  url:      string;
  healthy:  boolean;
  requests: number;
}

const pools: Record<"hint" | "summary", SpaceState[]> = {
  hint: config.spaces.hint.map(url => ({
    url, healthy: true, requests: 0
  })),
  summary: config.spaces.summary.map(url => ({
    url, healthy: true, requests: 0
  })),
};

// Pick a space that is healthy AND under the concurrency cap
function pick(service: "hint" | "summary"): SpaceState | null {
  const available = pools[service].filter(
    s => s.healthy && s.requests < MAX_CONCURRENT
  );
  if (available.length === 0) return null;
  // pick the one with fewest active requests
  return available.reduce((a, b) => a.requests <= b.requests ? a : b);
}

async function refreshHealth(service: "hint" | "summary"): Promise<void> {
  await Promise.allSettled(
    pools[service].map(async s => {
      try {
        const r = await fetch(`${s.url}/health`, {
          signal: AbortSignal.timeout(3000)
        });
        s.healthy = r.ok;
      } catch {
        s.healthy = false;
      }
    })
  );
}

async function callSpace(
  space: SpaceState,
  path: string,
  body: unknown,
  timeoutMs: number,
): Promise<unknown> {
  space.requests++;
  try {
    const res = await fetch(`${space.url}${path}`, {
      method: "POST",
      headers: {
        "Content-Type":  "application/json",
        "Authorization": `Bearer ${config.internalToken}`,
      },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(timeoutMs),
    });

    if (!res.ok) {
      space.healthy = false;
      throw new Error(`Space returned ${res.status}`);
    }

    return await res.json();
  } catch (err) {
    space.healthy = false;
    throw err;
  } finally {
    space.requests = Math.max(0, space.requests - 1);
  }
}

export async function forwardToSpace(
  service: "hint" | "summary",
  path: string,
  body: unknown
): Promise<{ data: unknown; spaceUsed: string }> {
  const timeoutMs = service === "summary"
    ? config.lb.summaryTimeoutMs
    : config.lb.timeoutMs;

  await refreshHealth(service);

  const primary = pick(service);

  if (primary) {
    try {
      const data = await callSpace(primary, path, body, timeoutMs);
      return { data, spaceUsed: primary.url };
    } catch {
      // primary failed — fall through to fallback below
    }
  }

  // primary full or failed — try any other available space
  const fallback = pools[service].find(
    s => s.url !== primary?.url && s.healthy && s.requests < MAX_CONCURRENT
  );

  if (fallback) {
    const data = await callSpace(fallback, path, body, timeoutMs);
    return { data, spaceUsed: `${fallback.url} (fallback)` };
  }

  throw new Error(
    `All ${service} spaces are full or unhealthy — ` +
    pools[service].map(s => `${s.url}: ${s.requests} reqs, healthy=${s.healthy}`).join(" | ")
  );
}

export function getPoolStatus() {
  return {
    hint:    pools.hint.map(({ url, healthy, requests }) => ({ url, healthy, requests })),
    summary: pools.summary.map(({ url, healthy, requests }) => ({ url, healthy, requests })),
  };
}