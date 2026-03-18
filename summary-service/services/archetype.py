def classify_archetype(rounds: list[dict], final: dict) -> str:
    if not rounds:
        # fallback to final state only
        rounds = [final]

    avg_itr  = sum(r.get("itr", 2)  for r in rounds) / len(rounds)
    avg_rnd  = sum(r.get("rnd", 2)  for r in rounds) / len(rounds)
    avg_spd  = sum(r.get("spd", 30) for r in rounds) / len(rounds)
    avg_tar  = sum(r.get("tar", 5)  for r in rounds) / len(rounds)
    avg_wfr  = sum(r.get("wfr", 10) for r in rounds) / len(rounds)
    prt_used = sum(1 for r in rounds if r.get("prt", False))

    final_inf  = final.get("inf", 0)
    final_inn  = final.get("inn", 0)
    final_dbt  = final.get("dbt", 0)
    final_mood = final.get("mood", 50)

    if prt_used >= 3 and final_inf > 15:
        return "The Populist"
    if avg_itr > 10 and final_inf < 6:
        return "The Inflation Hawk"
    if avg_rnd > 12 and final_inn > 75:
        return "The Tech Visionary"
    if final_dbt > 80 and final_inn > 60:
        return "The Debt Architect"
    if avg_tar > 35 and final.get("trd", 0) < 2:
        return "The Isolationist"
    if avg_wfr > 65:
        return "The Gambler"
    return "The Balanced Steward"