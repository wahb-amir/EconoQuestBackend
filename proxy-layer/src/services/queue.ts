import WebSocket from "ws";
import { config } from "../config.js";

// ── Space state ───────────────────────────────────────────────────────────────

export interface SpaceState {
  id: string;
  url: string;
  busy: boolean;
  healthy: boolean;
}

export const hintSpaces: SpaceState[] = [
  { id: "hint-1", url: config.spaces.hint[0], busy: false, healthy: true },
  { id: "hint-2", url: config.spaces.hint[1], busy: false, healthy: true },
];

export function getFreeSpace(): SpaceState | null {
  return hintSpaces.find((s) => !s.busy && s.healthy) ?? null;
}

export function markBusy(spaceId: string): void {
  const s = hintSpaces.find((s) => s.id === spaceId);
  if (s) s.busy = true;
}

export function markFree(spaceId: string): void {
  const s = hintSpaces.find((s) => s.id === spaceId);
  if (s) s.busy = false;
}

export function markHealthy(spaceId: string, healthy: boolean): void {
  const s = hintSpaces.find((s) => s.id === spaceId);
  if (s) s.healthy = healthy;
}

// ── Request queue ─────────────────────────────────────────────────────────────

export interface QueuedRequest {
  ws: WebSocket;
  body: unknown;
  cacheKey: string;
  userId: string;
  resolve: () => void;
}

const queue: QueuedRequest[] = [];

export function enqueue(req: QueuedRequest): number {
  queue.push(req);
  return queue.length;
}

export function processQueue(): void {
  if (queue.length === 0) return;

  const freeSpace = getFreeSpace();
  if (!freeSpace) return;

  const next = queue.shift();
  if (!next) return;

  // notify remaining clients of updated positions
  queue.forEach((req, i) => {
    if (req.ws.readyState === WebSocket.OPEN) {
      req.ws.send(JSON.stringify({ type: "queued", position: i + 1 }));
    }
  });

  // resolve so the waiting async handler resumes
  next.resolve();
}

export function getQueueStatus() {
  return {
    spaces: hintSpaces.map(({ id, busy, healthy }) => ({ id, busy, healthy })),
    queueLength: queue.length,
  };
}
