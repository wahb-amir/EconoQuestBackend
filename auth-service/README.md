---
title: Auth Service
emoji: 🔥
colorFrom: purple
colorTo: purple
sdk: docker
pinned: false
---

# EconoQuest — Auth Service

FastAPI authentication service handling user registration, login, OAuth, session management, and score submission. Runs on HuggingFace Spaces (CPU free tier).

## Responsibilities

- Email/password registration and login via Supabase Auth
- Google and GitHub OAuth flows
- httpOnly cookie management (`access_token` + `refresh_token`)
- JWT validation and session refresh
- Cross-domain token endpoint for WebSocket auth
- Score submission to the leaderboard via Supabase RPC

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/register` | Create account + auto sign-in |
| POST | `/auth/login` | Email/password login |
| POST | `/auth/logout` | Clear session cookies |
| POST | `/auth/refresh` | Rotate tokens using refresh cookie |
| GET  | `/auth/me` | Return current user from cookie |
| GET  | `/auth/token` | Return access token in body (for cross-domain WS) |
| POST | `/auth/set-session` | Set cookies from OAuth token pair |
| POST | `/auth/submit-score` | Upsert score to leaderboard |
| GET  | `/auth/google` | Initiate Google OAuth |
| GET  | `/auth/github` | Initiate GitHub OAuth |
| GET  | `/auth/callback` | PKCE code exchange (server-side) |
| GET  | `/health` | Health check |

## Cookie Strategy

Cookies are set with `httpOnly=True`, `secure=True`, `samesite=lax`. The frontend proxies all auth requests through a Next.js API route (`/api/auth/*`) so cookies land on the frontend domain rather than the HF Space domain — this prevents them from being dropped on page reload.

## Local Development

```bash
cd auth-service
pip install -r requirements.txt
cp .env.example .env
# fill in .env values
uvicorn app:app --reload --port 8001
```

## HuggingFace Deployment

```bash
git subtree split --prefix=auth-service -b auth-deploy
git push hf-auth auth-deploy:main --force
git branch -D auth-deploy
```

Add the remote once:
```bash
git remote add hf-auth https://huggingface.co/spaces/YOUR_HF_USERNAME/auth-service
```

## Environment Variables

See `.env.example` below. All variables must be set as **Secrets** in HF Space settings (not Variables — Secrets are not exposed in logs).

## Dependencies

- `fastapi` — web framework
- `supabase` — Supabase Python client
- `python-dotenv` — local env loading
- `uvicorn` — ASGI server