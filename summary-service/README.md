---
title: Summery 1
emoji: 🚀
colorFrom: blue
colorTo: red
sdk: docker
proxy_timeout: 290
pinned: false
---
# EconoQuest — Summary Service

FastAPI inference service that generates per-round economic summaries and classifies player archetypes at game end. Uses Qwen2.5-1.5B-Instruct. Deployed as two identical instances on HuggingFace Spaces for load balancing.

## Responsibilities

- Generate a 1-sentence economic analysis of each round's decisions and outcomes
- Save round summaries to Supabase keyed by `session_id` and `round`
- At game end, retrieve all stored rounds for a session and classify the player archetype
- Archetype classification uses pure Python logic (no inference) — checks final metric thresholds

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/round-summary` | Internal token | Generate + store 1 round summary |
| POST | `/summary` | Internal token | Retrieve all rounds + classify archetype |
| GET  | `/health` | None | Health check |

All POST endpoints require `Authorization: Bearer <INTERNAL_TOKEN>` header.

## Round Summary Flow

Called in the background after each round advance (fire-and-forget from frontend):

```
POST /round-summary {
  session_id: "uuid-v4-stable-per-game",
  state: { round, ctx, itr, spd, rnd, fln, wfr, tar, prt,
           gdp, inf, unemp, dbt, cur, trd, inn, sal, mood, swf }
}
→ Qwen generates 1-sentence analysis of the economic situation
→ saves to econoquest_round_summaries (session_id, round, summary)
→ unique(session_id, round) — safe to retry
```

## Final Summary Flow

Called once when the player opens the mandate review screen:

```
POST /summary {
  session_id: "uuid-v4-stable-per-game",
  final_state: { ... same 18 fields ... }
}
→ retrieves all rows from econoquest_round_summaries WHERE session_id = ?
→ classifies archetype from final_state metrics (pure logic)
→ returns { archetype, round_summaries: [{round, summary}, ...] }
```

## Archetype Classification Logic

Checks most extreme conditions first (order matters):

| Archetype | Trigger |
|-----------|---------|
| The Populist | `final_inf > 20` OR `prt_rounds >= 3` |
| The Debt Architect | `final_unemp > 20` AND `final_dbt > 100` |
| The Inflation Hawk | `avg_itr > 10` AND `final_inf < 6` |
| The Tech Visionary | `avg_rnd > 12` AND `final_inn > 75` |
| The Debt Architect (alt) | `final_dbt > 80` AND `final_inn > 60` |
| The Isolationist | `avg_tar > 35` AND `final_trd < 2` |
| The Gambler | `avg_wfr > 65` |
| The Balanced Steward | default fallback |

## Supabase Schema

```sql
create table econoquest_round_summaries (
  id         bigserial primary key,
  session_id text not null,
  round      integer not null,
  summary    text not null,
  state      jsonb,
  created_at timestamptz default now(),
  unique(session_id, round)
);
```

## Local Development

```bash
cd summary-service
pip install -r requirements.txt
cp .env.example .env
# fill in .env values
uvicorn app:app --reload --port 8003
```

Models download on first run (~1.5GB for Qwen2.5-1.5B). Cached after first download.

## HuggingFace Deployment

```bash
git subtree split --prefix=summary-service -b summary-deploy
git push hf-summary-1 summary-deploy:main --force
git push hf-summary-2 summary-deploy:main --force
git branch -D summary-deploy
```

Add remotes once:
```bash
git remote add hf-summary-1 https://huggingface.co/spaces/YOUR_HF_USERNAME/summary-1
git remote add hf-summary-2 https://huggingface.co/spaces/YOUR_HF_USERNAME/summary-2
```

## Environment Variables

See `.env.example`. Set as **Secrets** in each HF Space.
