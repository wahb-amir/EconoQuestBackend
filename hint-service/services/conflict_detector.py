def detect_conflicts(s: dict) -> list[dict]:
    c = []

    ctx  = s.get("ctx", 25)
    itr  = s.get("itr", 2)
    spd  = s.get("spd", 30)
    rnd  = s.get("rnd", 2)
    fln  = s.get("fln", 0)
    wfr  = s.get("wfr", 10)
    tar  = s.get("tar", 5)
    prt  = s.get("prt", False)
    inf  = s.get("inf", 0)
    dbt  = s.get("dbt", 0)
    trd  = s.get("trd", 0)
    mood = s.get("mood", 100)

    if rnd > 10 and spd < 20:
        c.append({
            "key": "rnd_no_base",
            "message": "High R&D with low public spending — innovation needs infrastructure to convert to real output."
        })

    if prt and inf > 8:
        c.append({
            "key": "prt_inf",
            "message": "Printing currency while inflation is already elevated will compound purchasing power erosion rapidly."
        })

    if prt and itr < 1:
        c.append({
            "key": "prt_zero_itr",
            "message": "Printing money with near-zero interest rates removes the only brake on hyperinflation."
        })

    if tar > 40 and fln > 20:
        c.append({
            "key": "tar_fln",
            "message": "High tariffs signal protectionism but foreign lending creates geopolitical exposure — these goals work against each other."
        })

    if ctx < 5 and spd > 60:
        c.append({
            "key": "zero_tax_spend",
            "message": "Near-zero corporate tax with high spending creates a widening revenue gap that forces borrowing or printing."
        })

    if itr > 15 and spd > 70:
        c.append({
            "key": "itr_spd",
            "message": "High interest rates contract the economy while high spending stimulates it — these cancel each other at significant fiscal cost."
        })

    if wfr > 80 and dbt > 70:
        c.append({
            "key": "wfr_dbt",
            "message": "Maximum wealth fund risk while national debt is high leaves no safety net if the fund underperforms."
        })

    if tar > 60 and trd < -2:
        c.append({
            "key": "tar_trd_fail",
            "message": "High tariffs have not fixed your trade deficit — likely facing retaliation or domestic supply gaps."
        })

    if ctx > 70 and mood < 50:
        c.append({
            "key": "high_ctx_mood",
            "message": "Very high corporate tax with low public mood risks capital flight — businesses may relocate."
        })

    return c