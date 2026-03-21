import os
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from services.auth import verify_internal_token
from services.embeddings import embed_state, get_model
from services.retrieval import retrieve_chunks
from services.conflict_detector import detect_conflicts
from services.prompt_builder import build_hint_prompt
from services.inference import generate_hint, generate_hint_stream

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[startup] preloading embedding model...")
    get_model()
    print("[startup] ready")
    yield
    print("[shutdown] done")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlayerState(BaseModel):
    round:  int
    nation: str   = "unnamed"
    ctx:    float = 25.0
    itr:    float = 2.0
    spd:    float = 30.0
    rnd:    float = 2.0
    fln:    float = 0.0
    wfr:    float = 10.0
    tar:    float = 5.0
    prt:    bool  = False
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

@app.get("/health")
async def health():
    return {"status": "ok", "service": "hint-service"}

@app.post("/hint")
async def hint(
    req: HintRequest,
    _: bool = Depends(verify_internal_token)
):
    state_dict = req.state.model_dump()
    conflicts  = detect_conflicts(state_dict)
    embedding  = embed_state(state_dict)
    chunks     = retrieve_chunks(embedding, count=3)
    prompt     = build_hint_prompt(state_dict, chunks, conflicts)
    hint_text  = generate_hint(prompt)

    return {
        "hint":        hint_text,
        "conflicts":   conflicts,
        "chunks_used": [c["chunk_key"] for c in chunks],
    }

@app.post("/hint-stream")
async def hint_stream(
    req: HintRequest,
    _: bool = Depends(verify_internal_token)
):
    state_dict = req.state.model_dump()
    conflicts  = detect_conflicts(state_dict)
    embedding  = embed_state(state_dict)
    chunks     = retrieve_chunks(embedding, count=3)
    prompt     = build_hint_prompt(state_dict, chunks, conflicts)

    def token_generator():
        meta = json.dumps({
            "type":        "meta",
            "conflicts":   conflicts,
            "chunks_used": [c["chunk_key"] for c in chunks]
        })
        yield f"data: {meta}\n\n"

        for word in generate_hint_stream(prompt):
            chunk = json.dumps({"type": "token", "text": word})
            yield f"data: {chunk}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        token_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control":     "no-cache",
            "X-Accel-Buffering": "no",
        }
    )