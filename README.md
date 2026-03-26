# EconoQuest Backend

A distributed microservices architecture for an economic simulation game with AI-powered hints and analysis. All services are deployed on HuggingFace Spaces with a Fastify proxy layer orchestrating requests from the frontend.

## Architecture Overview

```
Frontend (Next.js)
    ↓
Proxy Layer (Fastify)
    ├── WebSocket → Hint Service ×2 (FastAPI)
    ├── HTTP → Summary Service ×2 (FastAPI)
    ├── HTTP → Auth Service (FastAPI)
    └── Health cron pings all services
    
Backend Services:
├── Auth Service (HF Space CPU)
├── Hint Service ×2 (HF Space CPU, load balanced)
├── Summary Service ×2 (HF Space CPU, load balanced)
└── Proxy Layer (HF Space CPU)

Data:
└── Supabase (PostgreSQL + pgvector, JWT auth, cache storage)
```

## Services

### 1. **Auth Service** (`/auth-service`)
FastAPI authentication & session management. Handles user registration, OAuth (Google/GitHub), JWT token lifecycle, and leaderboard score submission.

**Key Responsibilities:**
- Email/password authentication via Supabase Auth
- OAuth 2.0 flows with PKCE
- httpOnly cookie management (access + refresh tokens)
- Cross-domain token endpoint for WebSocket auth
- Score submission to leaderboard

**Deployment:** HuggingFace Spaces (CPU free tier, single instance)  
**Port:** 8001  
**Details:** See [`auth-service/README.md`](auth-service/README.md)

---

### 2. **Hint Service** (`/hint-service` — 2 instances)
FastAPI RAG inference service that generates Socratic economic questions using Groq's Llama 3.3 70B model. Retrieves relevant knowledge chunks via pgvector similarity search.

**Key Responsibilities:**
- Embed player game state using `sentence-transformers/all-MiniLM-L6-v2`
- Retrieve top 3 relevant knowledge chunks from Supabase pgvector
- Detect policy conflicts in player decisions
- Call Groq API (Llama 3.3 70B) to generate Socratic hints
- Stream responses word-by-word via SSE
- Cache hints in Supabase for common game states

**Deployment:** HuggingFace Spaces ×2 (CPU free tier, load balanced)  
**Ports:** 8002 (hint-service-1), 8002 (hint-service-2)  
**API:** `/hint` (full response), `/hint-stream` (SSE stream)  
**Details:** See [`hint-service/README.md`](hint-service/README.md)

---

### 3. **Summary Service** (`/summary-service` — 2 instances)
FastAPI inference service that generates per-round economic analyses and classifies player archetypes at game end using Qwen2.5-1.5B-Instruct.

**Key Responsibilities:**
- Generate 1-sentence economic analysis per game round
- Store round summaries to Supabase (`econoquest_round_summaries`)
- Retrieve all rounds for a session and classify player archetype
- Archetype classification via pure Python logic (no inference needed)

**Deployment:** HuggingFace Spaces ×2 (CPU free tier, load balanced)  
**Ports:** 8003 (summary-service-1), 8003 (summary-service-2)  
**API:** `/round-summary` (generate + store), `/summary` (retrieve all + classify)  
**Details:** See [`summary-service/README.md`](summary-service/README.md)

---

### 4. **Proxy Layer** (`/proxy-layer`)
Fastify v4 proxy and orchestration layer. Single entry point for all frontend traffic. Handles WebSocket connections, load balancing, request queuing, LRU hint caching, and health monitoring.

**Key Responsibilities:**
- WebSocket endpoint for streaming hints (`/ws/hint`)
- HTTP fallback for hints and summaries
- Load balancing (least-connections) across hint-service ×2 and summary-service ×2
- LRU cache for hints (500 entries, SHA256 state hash as key)
- Request queue with position tracking when hint services are busy
- Health cron every 25 minutes to prevent cold starts
- Rate limiting (60 req/min global, 10 req/min on hint endpoints)

**Deployment:** HuggingFace Spaces (CPU free tier, single instance)  
**Port:** 7860 (default HF Space port)  
**Details:** See [`proxy-layer/README.md`](proxy-layer/README.md)

---

## Data Flow

### Hint Request (WebSocket)
```
Frontend
  → POST /ws/hint { token: JWT, state: {round, gdp, inf, ...} }
  → Proxy verifies JWT via Supabase
  → SHA256 hash state → check LRU cache in Supabase
      ✓ Cache hit → stream cached words at 35ms/word
      ✗ Cache miss → pick free hint Space (least connections)
                   → both busy? → enqueue + send position updates
                   → forward to /hint-stream (SSE)
                   → proxy each SSE token as WS message
                   → save full hint to cache
  ← WS messages { type: "token", text: "..." }
  ← { type: "done" } when complete
```

### Round Summary (Background)
```
Frontend (fire-and-forget after round advance)
  → POST /api/game/round-summary { session_id, state }
  → Proxy forwards to least-busy summary-service
  → Summary-service generates 1-sentence analysis via Qwen2.5-1.5B
  → Stores to econoquest_round_summaries (session_id, round, summary)
  → Returns immediately
```

### Final Summary (Mandate Review)
```
Frontend
  → POST /api/game/final-summary { session_id, final_state }
  → Proxy forwards to summary-service
  → Service retrieves all stored rounds from econoquest_round_summaries
  → Classifies archetype from final_state metrics (pure logic)
  → Returns { archetype, round_summaries: [{round, summary}, ...] }
```

---

## Knowledge Base

Hint service uses 99 knowledge chunks across 5 layers, stored in Supabase:

| Layer | File | Content |
|-------|------|---------|
| 1 | `layer1_mechanics.py` | Core policy → outcome relationships |
| 2 | `layer2_pairwise.py` | How two policies interact |
| 3 | `layer3_extremes.py` | Threshold / breaking point knowledge |
| 4 | `layer4_rounds.py` | Stage-specific advice (early/mid/late game) |
| 5 | `layer5_history.py` | Real-world economic archetype examples |

To embed chunks into Supabase (run once per environment):
```bash
curl https://your-hint-service.hf.space/embed \
  -H "Authorization: Bearer YOUR_INTERNAL_TOKEN"
```

---

## Local Development

Each service runs independently on its own port. Clone the repo and start them in any order:

```bash
# Terminal 1: Auth Service
cd auth-service
pip install -r requirements.txt
cp .env.example .env
# fill in .env values
uvicorn app:app --reload --port 8001

# Terminal 2: Hint Service
cd hint-service
pip install -r requirements.txt
cp .env.example .env
# fill in .env values
uvicorn app:app --reload --port 8002

# Terminal 3: Summary Service
cd summary-service
pip install -r requirements.txt
cp .env.example .env
# fill in .env values
uvicorn app:app --reload --port 8003

# Terminal 4: Proxy Layer
cd proxy-layer
pnpm install
cp .env.example .env
# fill in .env values
pnpm dev  # runs on port 7860
```

### Environment Variables

Each service requires a `.env` file. See the example files in each directory:
- `auth-service/.env.example`
- `hint-service/.env.example`
- `summary-service/.env.example`
- `proxy-layer/.env.example`

Key shared variables:
- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_KEY` — Supabase service role key
- `INTERNAL_TOKEN` — Shared auth token between proxy and inference services
- Service-specific: `GROQ_API_KEY` (hint-service only)

---

## HuggingFace Deployment

Each service deploys independently to its own HF Space. Add remotes once:

```bash
git remote add hf-auth https://huggingface.co/spaces/YOUR_HF_USERNAME/auth-service
git remote add hf-hint-1 https://huggingface.co/spaces/YOUR_HF_USERNAME/hint-service-1
git remote add hf-hint-2 https://huggingface.co/spaces/YOUR_HF_USERNAME/hint-service-2
git remote add hf-summary-1 https://huggingface.co/spaces/YOUR_HF_USERNAME/summary-1
git remote add hf-summary-2 https://huggingface.co/spaces/YOUR_HF_USERNAME/summary-2
git remote add hf-proxy https://huggingface.co/spaces/YOUR_HF_USERNAME/proxy-layer
```

Deploy each service:

```bash
# Auth Service
git subtree split --prefix=auth-service -b auth-deploy
git push hf-auth auth-deploy:main --force
git branch -D auth-deploy

# Hint Service 1
git subtree split --prefix=hint-service -b hint-deploy
git push hf-hint-1 hint-deploy:main --force
git branch -D hint-deploy

# Hint Service 2
git push hf-hint-2 hint-deploy:main --force

# Summary Service 1
git subtree split --prefix=summary-service -b summary-deploy
git push hf-summary-1 summary-deploy:main --force
git branch -D summary-deploy

# Summary Service 2
git push hf-summary-2 summary-deploy:main --force

# Proxy Layer
git subtree split --prefix=proxy-layer -b proxy-deploy
git push hf-proxy proxy-deploy:main --force
git branch -D proxy-deploy
```

---

## Keepalive Strategy

HuggingFace free-tier Spaces can cold-start in 30–60 seconds if unused. The proxy layer health cron pings all services every 25 minutes:

```
UptimeRobot (every 5 min) → GET /health on proxy
  ↓
Proxy health cron (every 25 min)
  → GET /health on hint-service-1
  → GET /health on hint-service-2
  → GET /health on summary-service-1
  → GET /health on summary-service-2
  → GET /health on auth-service
```

This keeps all services warm and responsive.

---

## Monitoring & Debugging

### Health Check
```bash
curl https://your-proxy.hf.space/health
```

### Service Status
```bash
curl https://your-proxy.hf.space/api/status
```

### Supabase Connectivity
```bash
curl https://your-proxy.hf.space/api/supabase-test
```

### Queue Status (Internal)
```bash
curl https://your-proxy.hf.space/internal/queue-status \
  -H "Authorization: Bearer YOUR_INTERNAL_TOKEN"
```

---

## Rate Limiting

Proxy layer enforces:
- **Global:** 60 requests/minute per IP
- **Hint endpoints:** 10 requests/minute per IP (`/hint`, `/hint-stream`)

---

## Caching Strategy

### Hint Cache (LRU)
- **Key:** SHA256 hash of 18 state values (player policies, metrics)
- **Size:** 500 entries max
- **Storage:** Supabase table `econoquest_hint_cache`
- **TTL:** No explicit TTL; uses LRU eviction

### Summary Cache
- Per-round summaries are stored in `econoquest_round_summaries` (no eviction)

---

## Technology Stack

| Service | Language | Framework | Key Libraries |
|---------|----------|-----------|---|
| Auth | Python | FastAPI | supabase-py, python-dotenv |
| Hint | Python | FastAPI | sentence-transformers, supabase-py |
| Summary | Python | FastAPI | transformers, torch, supabase-py |
| Proxy | TypeScript | Fastify v4 | @fastify/websocket, @supabase/supabase-js |

---

## Troubleshooting

### Services Not Communicating
1. Check `.env` files have matching `INTERNAL_TOKEN`
2. Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
3. Test Supabase connectivity: `curl /api/supabase-test` on proxy

### Hints Not Caching
1. Verify hint cache table exists in Supabase: `econoquest_hint_cache`
2. Check proxy has write permissions to Supabase

### Cold Starts
1. Ensure health cron is running on proxy (check logs)
2. Manually trigger health check: `curl /health` on proxy
3. UptimeRobot should ping proxy every 5 minutes

### WebSocket Timeout
1. Check proxy WebSocket timeout is set to >30s
2. Verify hint service can actually reach Groq API
3. Check rate limit isn't blocking hint-service requests

---

## Directory Structure

```
econoquest-backend/
├── auth-service/
│   ├── README.md
│   ├── .env.example
│   ├── requirements.txt
│   ├── app.py
│   └── ...
├── hint-service/
│   ├── README.md
│   ├── .env.example
│   ├── requirements.txt
│   ├── app.py
│   └── ...
├── summary-service/
│   ├── README.md
│   ├── .env.example
│   ├── requirements.txt
│   ├── app.py
│   └── ...
├── proxy-layer/
│   ├── README.md
│   ├── .env.example
│   ├── package.json
│   ├── index.ts
│   └── ...
└── README.md (this file)
```

---

## Next Steps

1. **Set up Supabase** — Create project, configure pgvector extension, set up auth
2. **Configure environment variables** — Copy `.env.example` to `.env` in each service
3. **Embed knowledge chunks** — Run hint-service `/embed` endpoint once
4. **Deploy to HuggingFace Spaces** — Follow deployment guide above
5. **Set up UptimeRobot** — Add proxy `/health` endpoint to monitoring

For detailed information on each service, see:
- [Auth Service](auth-service/README.md)
- [Hint Service](hint-service/README.md)
- [Summary Service](summary-service/README.md)
- [Proxy Layer](proxy-layer/README.md)
