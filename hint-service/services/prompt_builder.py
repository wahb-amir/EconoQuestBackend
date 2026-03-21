SYSTEM_PROMPT = """You are a sharp, experienced economic advisor reviewing a leader's decisions in real time.

Your job is to ask ONE short Socratic question (1-2 sentences max) that makes the leader stop and think about a consequence they may not have considered.

Rules:
- Ask about the SPECIFIC numbers in their situation — never generic theory
- Reference the tension between two of their metrics (e.g. high debt AND high spending)
- Sound like a mentor, not a textbook — direct, slightly challenging, never preachy
- Never explain what the answer is — only ask
- Never ask multiple questions — pick the sharpest one
- Never use phrases like "Gross Domestic Product", "monetary policy", "fiscal stimulus" — speak plainly

Good examples:
"With inflation already at 24% and you're still printing — what happens to salaries in real terms next quarter?"
"Your debt is at 55% and climbing — at what point does the interest payment start crowding out your spending plans?"
"Public mood is at 52 and falling — how long can you sustain this before it affects your policy options?"

Bad examples (never do this):
"What percentage increase in debt would be considered manageable?" — too generic
"What do you plan to change first?" — too vague
"At what percentage does borrowing exceed GDP?" — textbook, not situational
"""

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

def _most_urgent_problem(state: dict) -> tuple[str, str]:
    gdp   = state.get("gdp",   0)
    inf   = state.get("inf",   0)
    unemp = state.get("unemp", 0)
    dbt   = state.get("dbt",   0)
    mood  = state.get("mood",  50)
    cur   = state.get("cur",   100)

    problems = [
        (inf,        "inflation",         f"inflation at {inf}%"),
        (unemp,      "unemployment",      f"unemployment at {unemp}%"),
        (dbt,        "debt",              f"debt at {dbt}% of GDP"),
        (-mood,      "public mood",       f"public mood at {mood}/100"),
        (-gdp,       "GDP contraction",   f"GDP at {gdp}%"),
        (100 - cur,  "currency weakness", f"currency index at {cur}"),
    ]
    problems.sort(key=lambda x: x[0], reverse=True)
    return problems[0][1], problems[0][2]  # label, specific value string

QUESTION_ANGLES = [
    "what is causing it",
    "what the tradeoff of fixing it is",
    "what happens if it gets worse",
    "which policy lever you would pull first and why",
    "what you would sacrifice to fix it",
    "whether your other policies are making it worse",
]

def build_hint_prompt(state, chunks, conflicts):
    round_num = state.get("round", 1)
    focus_label, focus_value = _most_urgent_problem(state)
    top_chunk = chunks[0]["content"] if chunks else ""
    angle = QUESTION_ANGLES[(round_num - 1) % len(QUESTION_ANGLES)]

    conflict_text = ""
    if conflicts:
        msgs = [c["message"] for c in conflicts]
        conflict_text = "\nWarnings: " + "; ".join(msgs)

    return (
        f"Round {round_num} player stats:\n"
        f"GDP={state.get('gdp')}% Inflation={state.get('inf')}% "
        f"Unemployment={state.get('unemp')}% Debt={state.get('dbt')}% "
        f"Mood={state.get('mood')} Currency={state.get('cur')} "
        f"Spending={state.get('spd')}% Tax={state.get('ctx')}% "
        f"Printing={'yes' if state.get('prt') else 'no'}."
        f"{conflict_text}\n"
        f"Context: {top_chunk}\n\n"
        f"The player's biggest problem is {focus_value}. "
        f"Ask them one short question about {angle}. "
        f"Use the actual number {focus_value} in the question. "
        f"Say 'you' not 'your country'. "
        f"Stop at the question mark."
    )
def build_hint_prompt(
    state: dict,
    chunks: list[dict],
    conflicts: list[dict]
) -> str:
    round_num = state.get("round", 1)  # ← fix: get from state
    focus = _most_urgent_problem(state)  # ← fix: compute here
    top_chunk = chunks[0]["content"] if chunks else ""

    conflict_text = ""
    if conflicts:
        msgs = [c["message"] for c in conflicts]
        conflict_text = "\nWarnings: " + "; ".join(msgs)

    return (
        f"Round {round_num} player stats:\n"
        f"GDP={state.get('gdp')}% Inflation={state.get('inf')}% "
        f"Unemployment={state.get('unemp')}% Debt={state.get('dbt')}% "
        f"Mood={state.get('mood')} Currency={state.get('cur')} "
        f"Spending={state.get('spd')}% Tax={state.get('ctx')}% "
        f"Printing={'yes' if state.get('prt') else 'no'}."
        f"{conflict_text}\n"
        f"Context: {top_chunk}\n\n"
        f"The player's biggest problem is {focus}. "
        f"Ask them one short question about it."
    )