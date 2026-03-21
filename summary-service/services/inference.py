from groq import Groq
from services.embeddings import embed_state
from services.retrieval import retrieve_chunks
import os
import re

client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL_ID = "llama-3.3-70b-versatile"
PROMPT_VERSION = "v4"

FOCUS_ROTATION = [
    "inflation",
    "unemployment",
    "debt",
    "public mood",
    "currency",
    "trade balance",
    "innovation",
    "GDP",
]

def _build_summary_prompt(round_num: int, state: dict, chunks: list[dict]) -> str:
    focus = FOCUS_ROTATION[(round_num - 1) % len(FOCUS_ROTATION)]

    # pick most relevant chunk — prefer layer 3 (extreme conditions) and 5 (history)
    context = ""
    if chunks:
        preferred = next(
            (c for c in chunks if c.get("layer") in (3, 5)), chunks[0]
        )
        context = f"Context: {preferred['content']}\n"

    return (
        f"[{PROMPT_VERSION}] Round {round_num} economic results:\n"
        f"GDP={state.get('gdp')}% Inflation={state.get('inf')}% "
        f"Unemployment={state.get('unemp')}% Debt={state.get('dbt')}% "
        f"Mood={state.get('mood')} Innovation={state.get('inn')} "
        f"Currency={state.get('cur')} Printed={'yes' if state.get('prt') else 'no'}.\n"
        f"{context}"
        f"Write one sharp sentence focused on {focus}. "
        f"Use the actual numbers. Reference the context if relevant. "
        f"This is a fictional game — do not reference real-world events directly, "
        f"but you may draw loose parallels if the context mentions them."
    )

def generate_round_summary(round_num: int, state: dict) -> str:
    # RAG pipeline
    embedding = embed_state(state)
    chunks    = retrieve_chunks(embedding, count=3)
    prompt    = _build_summary_prompt(round_num, state, chunks)

    response = client.chat.completions.create(
    model=MODEL_ID,
    messages=[
        {
            "role": "system",
            "content": (
                "You are a blunt economic advisor summarizing one round of an economics game. "
                "Write exactly one sentence. Maximum 20 words. "
                "Never start with 'With'. Never start two summaries the same way. "
                "Use the actual numbers. Be direct. "
                "Forbidden words: indicating, signaling, reflecting, despite, amid, reminiscent, echoes, poses."
            )
        },
        {"role": "user", "content": prompt}
    ],
    max_tokens=60, 
    temperature=0.7,
)

    raw = response.choices[0].message.content.strip()
    sentences = re.split(r"(?<=[.!?])\s+", raw)
    return sentences[0].strip() if sentences else raw