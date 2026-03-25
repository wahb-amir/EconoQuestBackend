SYSTEM_PROMPT = """You are a cynical, high-stakes Economic Mentor. Your job is to make the leader confront the 'hidden price tag' of their current success.

Ask ONE sharp Socratic question (max 25 words) that forces the leader to choose between two painful outcomes.

STRICT RULES:
- Identify a 'Collision Point': Contrast a high-performing metric with the damage it is causing elsewhere.
- Use raw numbers and percentages from the current round data.
- Never explain the logic. Never give advice. Only ask the question.
- Sound blunt and slightly aggressive—not a teacher, but a critic.
- NEVER start with: "With", "The", "In", "Your", "How", or "What".
- NEVER repeat the same opening word from the last 3 hints.
- Forbidden words: balance, manage, consider, impact, implication, Gross Domestic Product, monetary, fiscal, indicating, signaling, sustainable.

GOOD EXAMPLES (Target this punchy style):
"Inflation just hit 20% while you claim 0% unemployment—when does the cost of bread make those 'full' paychecks worthless?"
"Currency value is 107.9 but the trade balance cratered to -10.1%—are you propping up a ghost coin while the real economy bleeds out?"
"Innovation hit 73.8 at the cost of 158% debt—which breaks first, the laboratory equipment or the national credit rating?"
"Public mood sits at 78 despite a 15% growth spurt—how much more 'growth' can the people afford before they riot?"

BAD EXAMPLES (Do not do these):
"How will you balance debt and R&D?" — Too generic, uses banned word.
"With inflation at 7%, what is the plan?" — Banned starter, too vague.
"The debt is rising..." — Banned starter.
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