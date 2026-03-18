import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from services.auth import verify_internal_token
from services.embeddings import embed_state, get_model
from services.retrieval import retrieve_chunks
from services.conflict_detector import detect_conflicts
from services.prompt_builder import build_hint_prompt
from services.inference import generate_hint, load_model

# preload both models on startup so first request is fast
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[startup] preloading models...")
    get_model()    # embedding model
    load_model()   # inference model
    print("[startup] all models ready")
    yield
    print("[shutdown] done")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # proxy handles auth — Space itself is open
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Models ────────────────────────────────────────────

class PlayerState(BaseModel):
    round:  int
    nation: str = "unnamed"
    # inputs
    ctx:    float = 25.0
    itr:    float = 2.0
    spd:    float = 30.0
    rnd:    float = 2.0
    fln:    float = 0.0
    wfr:    float = 10.0
    tar:    float = 5.0
    prt:    bool  = False
    # outputs
    swf:    float = 0.0
    gdp:    float = 0.0
    inf:    float = 0.0
    unemp:  float = 0.0
    dbt:    float = 0.0
    cur:    float = 100.0
    trd:    float = 0.0
    inn:    float = 0.0
    sal:    float = 0.0
    mood:   float = 50.0

class HintRequest(BaseModel):
    state: PlayerState

# ── Routes ────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "service": "hint-service"}

@app.post("/hint")
async def hint(
    req: HintRequest,
    _: bool = Depends(verify_internal_token)
):
    state_dict = req.state.model_dump()

    # 1. detect conflicts — free, pure logic
    conflicts = detect_conflicts(state_dict)

    # 2. embed the player's abnormal conditions
    embedding = embed_state(state_dict)

    # 3. retrieve top 3 relevant chunks from pgvector
    chunks = retrieve_chunks(embedding, count=3)

    # 4. build compressed prompt
    prompt = build_hint_prompt(state_dict, chunks, conflicts)

    # 5. run inference
    result = generate_hint(prompt)

    return {
        "hint":      result["hint"],
        "conflicts": conflicts,
        "usage":     result["usage"],
        "chunks_used": [c["chunk_key"] for c in chunks],
    }
    
    
    