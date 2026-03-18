from sentence_transformers import SentenceTransformer
from functools import lru_cache

# loaded once on startup, cached in memory
@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    print("[embeddings] loading all-MiniLM-L6-v2...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("[embeddings] model ready")
    return model

def embed(text: str) -> list[float]:
    model = get_model()
    return model.encode(text, normalize_embeddings=True).tolist()

# Build a retrieval query from player state
# Focus on what is abnormal — that is what matches your chunk triggers
def build_retrieval_query(state: dict) -> str:
    flags = []

    inf   = state.get("inf", 0)
    dbt   = state.get("dbt", 0)
    unemp = state.get("unemp", 0)
    mood  = state.get("mood", 100)
    cur   = state.get("cur", 100)
    gdp   = state.get("gdp", 0)
    ctx   = state.get("ctx", 25)
    prt   = state.get("prt", False)
    spd   = state.get("spd", 30)
    itr   = state.get("itr", 2)
    tar   = state.get("tar", 5)
    wfr   = state.get("wfr", 10)
    round_num = state.get("round", 1)

    # most critical conditions first — these must dominate the query
    if inf > 20:
        flags.append("hyperinflation currency collapse printing money")
    elif inf > 12:
        flags.append("high inflation rising prices")

    if prt:
        flags.append("printing currency money supply hyperinflation risk")

    if dbt > 85:
        flags.append("debt crisis bankruptcy spiral")
    elif dbt > 65:
        flags.append("high debt borrowing")

    if unemp > 15:
        flags.append("unemployment crisis jobs")
    if mood < 30:
        flags.append("public mood collapse instability")
    if cur < 75:
        flags.append("currency collapse weak exchange rate")
    if gdp < -2:
        flags.append("recession economic contraction")
    if ctx < 5:
        flags.append("zero tax revenue gap spending")
    if spd > 75:
        flags.append("overspending fiscal pressure")
    if itr < 0.5:
        flags.append("zero interest rate floor inflation risk")
    if tar > 40:
        flags.append("high tariffs protectionism retaliation")
    if wfr > 80:
        flags.append("high risk wealth fund volatile")

    # round context
    if round_num <= 2:
        flags.append("early game investment foundation")
    elif round_num >= 6:
        flags.append("late game final rounds score")

    # fallback if nothing critical
    if not flags:
        flags.append("economic optimization balanced strategy")

    return " ".join(flags)
def embed_state(state: dict) -> list[float]:
    query = build_retrieval_query(state)
    print(f"[embeddings] query: {query}")
    return embed(query)