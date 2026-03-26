---
title: Hint Service 1
emoji: 👀
colorFrom: indigo
colorTo: yellow
sdk: docker
pinned: false
---
# EconoQuest — Hint Service
FastAPI inference service that generates Socratic economic questions using Groq's Llama 3.3 70B Versatile model via API. Uses RAG (Retrieval-Augmented Generation) with pgvector to retrieve relevant economic knowledge chunks before generating hints. Deployed as two identical instances on HuggingFace Spaces for load balancing.

## Responsibilities
- Embed player state using `sentence-transformers/all-MiniLM-L6-v2`
- Retrieve top 3 relevant knowledge chunks from Supabase pgvector
- Detect policy conflicts (e.g. printing money + high inflation)
- Build a compressed prompt and call Groq API for generation
- Stream the response word-by-word via SSE (`/hint-stream`)
- Return full response in one call (`/hint`)

## Endpoints
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/hint` | Internal token | Full response (non-streaming) |
| POST | `/hint-stream` | Internal token | SSE word-by-word stream |
| GET  | `/health` | None | Health check |

All POST endpoints require `Authorization: Bearer <INTERNAL_TOKEN>` header. This token is shared between the proxy-layer and hint services and never exposed to the frontend.

## RAG Pipeline
```
Player state (18 values)
  → embed_state() using all-MiniLM-L6-v2 (384-dim)
  → pgvector similarity search against econoquest_chunks
  → top 3 chunks retrieved
  → detect_conflicts() checks known policy tension pairs
  → build_hint_prompt() assembles compressed context
  → Groq API (Llama 3.3 70B) generates Socratic question
  → clean_output() strips prompt echo, caps at 3 sentences
```

## Knowledge Base
99 chunks across 5 layers stored in Supabase:
| Layer | File | Content |
|-------|------|---------|
| 1 | `layer1_mechanics.py` | Core policy → outcome relationships |
| 2 | `layer2_pairwise.py` | How two policies interact |
| 3 | `layer3_extremes.py` | Threshold / breaking point knowledge |
| 4 | `layer4_rounds.py` | Stage-specific advice (early/mid/late game) |
| 5 | `layer5_history.py` | Real-world economic archetype examples |

To embed chunks into Supabase (run once):
```bash
curl https://your-hint-service.hf.space/embed \
  -H "Authorization: Bearer YOUR_INTERNAL_TOKEN"
```
Remove or disable the `/embed` endpoint after running.

## Streaming Strategy
`/hint-stream` calls Groq's API with the Llama 3.3 70B model, which returns the full response quickly. The response is then yielded word-by-word as SSE events for a streaming UI effect. Groq's inference speed (~200–500ms for typical hints) provides fast perceived streaming without needing manual token-by-token decoding.

SSE event format:
```
data: {"type":"meta","conflicts":[...],"chunks_used":["pair.prt_itr_low",...]}
data: {"type":"token","text":"Why "}
data: {"type":"token","text":"might "}
...
data: {"type":"done"}
```

## Local Development
```bash
cd hint-service
pip install -r requirements.txt
cp .env.example .env
# fill in .env values (including GROQ_API_KEY)
uvicorn app:app --reload --port 8002
```

Models are downloaded from HuggingFace Hub on first run (~90MB for embeddings). The Groq API key is used for inference, so no large model downloads are needed for generation.

## Environment Variables
See `.env.example`. Set as **Secrets** in each HF Space:
- `GROQ_API_KEY` – API key for Groq inference (new)
- `SUPABASE_URL` – Supabase project URL
- `SUPABASE_KEY` – Supabase service role key
- `INTERNAL_TOKEN` – Shared authentication token with proxy layer

## HuggingFace Deployment
Deploy to both spaces:
```bash
git subtree split --prefix=hint-service -b hint-deploy
git push hf-hint-1 hint-deploy:main --force
git push hf-hint-2 hint-deploy:main --force
git branch -D hint-deploy
```

Add remotes once:
```bash
git remote add hf-hint-1 https://huggingface.co/spaces/YOUR_HF_USERNAME/hint-service-1
git remote add hf-hint-2 https://huggingface.co/spaces/YOUR_HF_USERNAME/hint-service-2
```