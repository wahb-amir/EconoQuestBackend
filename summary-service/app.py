import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

from services.auth import verify_internal_token
from services.archetype import classify_archetype
from services.inference import generate_round_summary, load_model

def get_supabase():
    return create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_SERVICE_KEY")
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[startup] preloading model...")
    load_model()
    print("[startup] ready")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RoundState(BaseModel):
    round:  int   = 1
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

class RoundSummaryRequest(BaseModel):
    session_id: str
    state:      RoundState

class FinalSummaryRequest(BaseModel):
    session_id:  str
    final_state: RoundState

@app.get("/health")
async def health():
    return {"status": "ok", "service": "summary-service"}

@app.post("/round-summary")
async def round_summary(
    req: RoundSummaryRequest,
    _: bool = Depends(verify_internal_token)
):
    state_dict = req.state.model_dump()
    summary = generate_round_summary(req.state.round, state_dict)
    supabase = get_supabase()
    supabase.table("econoquest_round_summaries").upsert({
        "session_id": req.session_id,
        "round":      req.state.round,
        "summary":    summary,
        "state":      state_dict,
    }, on_conflict="session_id,round").execute()
    return {"round": req.state.round, "summary": summary}

@app.post("/summary")
async def final_summary(
    req: FinalSummaryRequest,
    _: bool = Depends(verify_internal_token)
):
    supabase = get_supabase()
    result = supabase.table("econoquest_round_summaries") \
        .select("round, summary, state") \
        .eq("session_id", req.session_id) \
        .order("round") \
        .execute()
    round_summaries = result.data or []
    all_states = [r["state"] for r in round_summaries]
    final_dict = req.final_state.model_dump()
    archetype = classify_archetype(all_states, final_dict)
    return {
        "archetype":       archetype,
        "round_summaries": [
            {"round": r["round"], "summary": r["summary"]}
            for r in round_summaries
        ],
        "final_state": final_dict,
    }
