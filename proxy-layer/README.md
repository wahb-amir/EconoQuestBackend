---
title: Proxy Layer
emoji: 🌍
colorFrom: yellow
colorTo: yellow
sdk: docker
pinned: false
---

# EconoQuest — Proxy Layer

Fastify v4 proxy and orchestration layer. Acts as the single entry point for all game traffic from the frontend. Handles WebSocket connections for AI hints, load balances across HF Spaces, manages a request queue, maintains an LRU hint cache, and pings all services on a health cron.

## Responsibilities

- **WebSocket endpoint** (`/ws/hint`) — verifies Supabase JWT, checks LRU cache, queues or routes to a free hint Space, streams tokens back to the client
- **Load balancing** — least-connections across hint-service ×2 and summary-service ×2
- **LRU cache** — SHA256 hash of 18 state values as cache key, 500-entry limit, stored in Supabase
- **Queue** — when both hint Spaces are busy, requests wait and receive position updates
- **Summary routing** — forwards round-summary and final-summary requests to summary-service
- **Health cron** — pings all 5 HF Spaces + auth-service every 25 minutes to prevent cold starts
- **Rate limiting** — 60 req/min global, 10 req/min on hint endpoints (per IP)
- **Internal endpoints** — queue status, space-free callback, Supabase connectivity test

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| WS | `/ws/hint` | Supabase JWT (in message) | Streaming AI hint via WebSocket |
| POST | `/api/game/hint` | Supabase JWT | HTTP fallback hint (non-streaming) |
| POST | `/api/game/round-summary` | Supabase JWT | Store round analysis |
| POST | `/api/game/final-summary` | Supabase JWT | Retrieve full mandate review |
| GET | `/health` | None | Health check (used by UptimeRobot) |
| GET | `/api/status` | None | Pool status + space health |
| GET | `/api/supabase-test` | None | Supabase connectivity debug |
| GET | `/internal/queue-status` | Internal token | Queue + space busy state |
| POST | `/internal/space-free` | Internal token | Called by hint Space when request completes |

## WebSocket Flow

```
Client → wss://proxy/ws/hint
  → send { token: "eyJ...", state: { round, gdp, inf, ... } }
  → proxy verifies token via Supabase auth.getUser()
  → SHA256 hash state → check hint cache in Supabase
      cache hit  → stream cached words at 35ms/word
      cache miss → pick free hint Space (least connections)
                 → both busy: enqueue, send { type:"queued", position:N }
                 → forward to hint-space /hint-stream (SSE)
                 → proxy each SSE token as WS message: { type:"token", text:"..." }
                 → on done: save full hint to cache
```

## Keepalive Chain

```
UptimeRobot (every 5 min)
  → GET /health on proxy

healthCron (every 25 min, runs inside proxy)
  → GET /health on hint-service-1
  → GET /health on hint-service-2
  → GET /health on summary-service-1
  → GET /health on summary-service-2
  → GET /health on auth-service
```
This keeps all HF free-tier Spaces warm and prevents 30-60s cold start delays.

## Local Development

```bash
cd proxy-layer
pnpm install
cp .env.example .env
# fill in .env values
pnpm dev
```

Runs on port 7860 by default (matches HF Space port).

## HuggingFace Deployment

```bash
git subtree split --prefix=proxy-layer -b proxy-deploy
git push hf-proxy proxy-deploy:main --force
git branch -D proxy-deploy
```

Add remote once:
```bash
git remote add hf-proxy https://huggingface.co/spaces/YOUR_HF_USERNAME/proxy-layer
```

## Key Dependencies

- `fastify@4` — web framework
- `@fastify/websocket@8` — WebSocket support (v8 required for Fastify v4)
- `@fastify/rate-limit@8` — rate limiting (v8 required for Fastify v4)
- `@fastify/cors` — CORS
- `@supabase/supabase-js` — JWT verification + cache reads/writes
- `node-cron` — health ping scheduler

## Environment Variables

See `.env.example`. Set as **Secrets** in HF Space settings. The `SUPABASE_SERVICE_KEY` must be the `service_role` key with no newlines or trailing spaces — copy it directly from Supabase and paste as a single line.
