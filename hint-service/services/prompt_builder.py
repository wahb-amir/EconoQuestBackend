SYSTEM_PROMPT = (
    "You are a sharp Socratic economics advisor in a simulation game. "
    "Study the player's economic data and ask ONE pointed question. "
    "Address the player directly as 'you' — never say 'your country'. "
    "Never give advice. Never explain. Never answer. Never add notes. "
    "Output only the question itself. Nothing before it. Nothing after it. "
    "Stop after the question mark."
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

def _most_urgent_problem(state: dict) -> str:
    """Identify the single most alarming metric to focus the question on."""
    gdp   = state.get("gdp",   0)
    inf   = state.get("inf",   0)
    unemp = state.get("unemp", 0)
    dbt   = state.get("dbt",   0)
    mood  = state.get("mood",  50)
    cur   = state.get("cur",   100)

    problems = [
        (inf,          "inflation is spiralling"),
        (unemp,        "unemployment is critically high"),
        (dbt,          "debt is unsustainable"),
        (-mood,        "public mood is collapsing"),
        (-gdp,         "GDP is contracting"),
        (100 - cur,    "currency is severely weakened"),
    ]
    problems.sort(key=lambda x: x[0], reverse=True)
    return problems[0][1]

def build_hint_prompt(
    state: dict,
    chunks: list[dict],
    conflicts: list[dict]
) -> str:
    top_chunk = chunks[0]["content"] if chunks else ""
    urgent = _most_urgent_problem(state)

    conflict_text = ""
    if conflicts:
        msgs = [c["message"] for c in conflicts]
        conflict_text = "\nActive warnings:\n" + "\n".join(f"- {m}" for m in msgs)

    return (
        f"The player's economy right now:\n\n"
        f"{compress_state(state)}"
        f"{conflict_text}\n\n"
        f"The most urgent problem is: {urgent}.\n\n"
        f"Relevant context: {top_chunk}\n\n"
        f"Ask the player ONE Socratic question focused on '{urgent}'. "
        f"Output the question only. No second question. No notes. No explanation. "
        f"Stop after the question mark."
        f"Do not mention other metrics. One question only. No preamble."
    )