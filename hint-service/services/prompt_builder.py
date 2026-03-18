SYSTEM_PROMPT = (
    "You are a Socratic economics tutor in a simulation game. "
    "Your only job is to ask the player ONE short question (max 2 sentences) "
    "that makes them think about their current problem. "
    "Never give the answer. Never explain. Only ask a question."
)

def compress_state(s: dict) -> str:
    prt = "YES" if s.get("prt") else "NO"
    return (
        f"Round: {s.get('round', 1)}\n"
        f"Corporate Tax: {s.get('ctx', 25)}%\n"
        f"Interest Rate: {s.get('itr', 2)}%\n"
        f"Public Spending: {s.get('spd', 30)}% of GDP\n"
        f"R&D: {s.get('rnd', 2)}%\n"
        f"Tariff: {s.get('tar', 5)}%\n"
        f"Printing Money: {prt}\n"
        f"GDP Growth: {s.get('gdp', 0)}%\n"
        f"Inflation: {s.get('inf', 0)}%\n"
        f"Unemployment: {s.get('unemp', 0)}%\n"
        f"Debt/GDP: {s.get('dbt', 0)}%\n"
        f"Currency Index: {s.get('cur', 100)}\n"
        f"Public Mood: {s.get('mood', 50)}/100\n"
        f"Innovation: {s.get('inn', 0)} pts\n"
        f"Avg Salary: ${s.get('sal', 0):,}\n"
        f"Wealth Fund: ${s.get('swf', 0)}B"
    )

def build_hint_prompt(
    state: dict,
    chunks: list[dict],
    conflicts: list[dict]
) -> str:
    # pick the single most relevant chunk only
    top_chunk = chunks[0]["content"] if chunks else ""

    conflict_text = ""
    if conflicts:
        msgs = [c["message"] for c in conflicts]
        conflict_text = "\nWarnings:\n" + "\n".join(f"- {m}" for m in msgs)

    return (
        f"The player's nation has these stats:\n\n"
        f"{compress_state(state)}"
        f"{conflict_text}\n\n"
        f"Relevant context: {top_chunk}\n\n"
        f"Ask the player one Socratic question about their most urgent problem."
    )