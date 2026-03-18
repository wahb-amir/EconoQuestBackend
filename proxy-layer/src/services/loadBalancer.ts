import { config } from "../config.js";

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

function pick(service: "hint" | "summary"): SpaceState {
  const healthy = pools[service].filter(s => s.healthy);
  if (healthy.length === 0) return pools[service][0]; // try anyway
  return healthy.reduce((a, b) => a.requests <= b.requests ? a : b);
}

export async function forwardToSpace(
  service: "hint" | "summary",
  path: string,
  body: unknown
): Promise<{ data: unknown; spaceUsed: string }> {
  const timeoutMs = service === "summary"
    ? config.lb.summaryTimeoutMs
    : config.lb.timeoutMs;

  const spaces = pools[service];

  // refresh health in background
  await Promise.allSettled(
    spaces.map(async s => {
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

  const space = pick(service);
  space.requests++;

  try {
    const res = await fetch(`${space.url}${path}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${config.internalToken}`,
      },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(timeoutMs),
    });

    if (!res.ok) {
      space.healthy = false;
      throw new Error(`Space returned ${res.status}`);
    }

    const data = await res.json();
    return { data, spaceUsed: space.url };

  } catch (err) {
    space.healthy = false;

    // try fallback
    const fallback = spaces.find(
      s => s.url !== space.url && s.healthy
    );

    if (fallback) {
      fallback.requests++;
      try {
        const res = await fetch(`${fallback.url}${path}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${config.internalToken}`,
          },
          body: JSON.stringify(body),
          signal: AbortSignal.timeout(timeoutMs),
        });
        const data = await res.json();
        return { data, spaceUsed: `${fallback.url}(fallback)` };
      } finally {
        fallback.requests--;
      }
    }

    throw err;
  } finally {
    space.requests = Math.max(0, space.requests - 1);
  }
}

export function getPoolStatus() {
  return {
    hint:    pools.hint.map(({ url, healthy, requests }) => ({ url, healthy, requests })),
    summary: pools.summary.map(({ url, healthy, requests }) => ({ url, healthy, requests })),
  };
}