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

    # Updated API Call Settings
    response = client.chat.completions.create(
    model=MODEL_ID,
    messages=[
        {
            "role": "system",
            "content": (
                "You are a blunt, data-driven Senior Economic Advisor. "
                "Analyze the round data and provide exactly two punchy sentences. "
                "Sentence 1: Link a player action directly to a specific metric shift using raw numbers. "
                "Sentence 2: Issue a cynical warning or a strategic pivot. "
                "\n\nSTRICT CONSTRAINTS:\n"
                "- Focus on the 'Golden Triangle': GDP Growth, CPI (Inflation), and Unemployment. "
                "- Ignore total debt unless it causes a specific credit crisis. "
                "- Use specific percentages and absolute numbers. "
                "- Never start with 'With', 'The', 'In', or 'Your'. "
                "- Forbidden words: indicating, signaling, reflecting, despite, amid, reminiscent, echoes, poses, transition, multifaceted, context."
            )
        },
        {"role": "user", "content": prompt}
    ],
    max_tokens=120, 
    temperature=0.8,        # Higher temp allows for more 'cynical' creative flair
    presence_penalty=0.6,   # Encourages the model to talk about new topics/metrics
    frequency_penalty=0.5,  # Strictly prevents repetitive sentence structures
)

    raw = response.choices[0].message.content.strip()
    sentences = re.split(r"(?<=[.!?])\s+", raw)
    return sentences[0].strip() if sentences else raw