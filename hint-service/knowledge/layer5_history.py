# Layer 5 — Historical analog + Hall of Fame seeds
# 10 historical + 5 seeded HOF runs

LAYER5 = [
    {
        "layer": 5,
        "chunk_key": "hist.weimar",
        "content": "hist:weimar_1921-23 pattern:prt_sustained+war_debt→inf>1000%. analog:prt_active+dbt>80+itr<2. outcome:cur_collapse sal_worthless society_breakdown. escape_was:new_currency+foreign_loan+austerity. in_game:stop_prt_itr↑_immediately.",
        "metadata": {"event": "weimar", "layer": 5}
    },
    {
        "layer": 5,
        "chunk_key": "hist.volcker",
        "content": "hist:volcker_1979-83 pattern:itr↑↑(20%)+inf_crushed. analog:inf>15 itr↑_aggressive. outcome:recession_deep unemp↑↑ then_stable_growth_decade. in_game:accept_gdp_sacrifice_for_inf_fix worth_it_if_r<5.",
        "metadata": {"event": "volcker", "layer": 5}
    },
    {
        "layer": 5,
        "chunk_key": "hist.oil_shock_1973",
        "content": "hist:1970s_oil_shock pattern:tar_equivalent+inf↑+gdp↓ stagflation. analog:tar>40+inf>10+gdp<1. outcome:policy_stuck itr↑_kills_gdp spd↑_worsens_inf. in_game:rnd↑_supply_side tar↓_gradual only_exit.",
        "metadata": {"event": "oil_shock", "layer": 5}
    },
    {
        "layer": 5,
        "chunk_key": "hist.japan_bubble",
        "content": "hist:japan_1990s pattern:asset_bubble_burst+deflation+lost_decade. analog:gdp<0+inf<1+dbt↑+inn_stagnant. outcome:spd↑_failed itr=0_failed structural_reform_only_worked. in_game:rnd↑+ctx_reform not_just_stimulus.",
        "metadata": {"event": "japan_bubble", "layer": 5}
    },
    {
        "layer": 5,
        "chunk_key": "hist.singapore",
        "content": "hist:singapore_model pattern:ctx_low+rnd_high+trd_open+inn↑. analog:ctx<20+rnd>10+tar<15+inn>70. outcome:gdp↑↑ sal↑ trd_surplus cur_strong. viable_if: dbt_controlled spd_efficient not_just_low.",
        "metadata": {"event": "singapore", "layer": 5}
    },
    {
        "layer": 5,
        "chunk_key": "hist.nordic",
        "content": "hist:nordic_model pattern:ctx_high+spd_high+inn_high+unemp_low. analog:ctx>45+spd>50+rnd>12+mood>75. viable_if: gdp>3 to_sustain_tax_base. inn_must_compensate_for_tax_burden. long_game_strategy.",
        "metadata": {"event": "nordic", "layer": 5}
    },
    {
        "layer": 5,
        "chunk_key": "hist.zimbabwe",
        "content": "hist:zimbabwe_2008 pattern:prt_extreme+dbt+political_crisis→inf_millions_percent. analog:prt_active+inf>20+mood<30+dbt>90. in_game:this_is_game_over_trajectory. only_hope:itr↑↑+prt_stop+foreign_aid(fln↑).",
        "metadata": {"event": "zimbabwe", "layer": 5}
    },
    {
        "layer": 5,
        "chunk_key": "hist.korea_miracle",
        "content": "hist:korea_1960-90 pattern:rnd↑+spd_infrastructure+tar_protect_early→inn↑↑ gdp↑↑. analog:r1-3 rnd>10+spd>35+tar>20_early then_tar↓+ctx_reform_later. payoff:inn>80+gdp>5+trd↑. timing_critical.",
        "metadata": {"event": "korea", "layer": 5}
    },
    {
        "layer": 5,
        "chunk_key": "hist.2008_crisis",
        "content": "hist:2008_gfc pattern:wfr_max+fln_high+swf_exposed→swf_collapse dbt↑↑. analog:wfr>80+fln>40+dbt>60. in_game:reduce_wfr_immediately fln↓ swf_buffer_protect. dont_chase_returns_when_exposed.",
        "metadata": {"event": "gfc_2008", "layer": 5}
    },
    {
        "layer": 5,
        "chunk_key": "hist.covid_response",
        "content": "hist:covid_2020 pattern:spd↑↑+itr↓+prt_equivalent→gdp_saved short then_inf_2021-23. analog:itr<1+spd>70+prt=1. in_game:exit_strategy_needed_r2 raise_itr_cut_spd before_inf_embeds.",
        "metadata": {"event": "covid", "layer": 5}
    },
    # Hall of Fame seeds — 5 top player strategy docs
    {
        "layer": 5,
        "chunk_key": "hof.balanced_steward_r7",
        "content": "hof:rank1 archetype:balanced_steward final_score:91. strategy: r1-2:rnd↑8+spd35+ctx28+itr2 built_foundation. r3-4:inn_payoff gdp↑4.2 dbt_stable48. r5:swf_build wfr30_moderate. r6-7:mood_consolidate sal↑ gentle_itr↑_inf_control. never_used_prt. key:patience_compounding.",
        "metadata": {"type": "hof", "layer": 5}
    },
    {
        "layer": 5,
        "chunk_key": "hof.tech_visionary_r7",
        "content": "hof:rank2 archetype:tech_visionary final_score:88. strategy: r1-3:rnd↑15+spd30_base sacrificed_gdp_short. r4:inn>75 gdp_bonus_activated. r5-7:harvest inn_dividend ctx↓18_attract_inv trd↑ cur_strong. unemp_stayed_high_r1-3_accepted_tradeoff.",
        "metadata": {"type": "hof", "layer": 5}
    },
    {
        "layer": 5,
        "chunk_key": "hof.hawk_inflation_r7",
        "content": "hof:rank3 archetype:inflation_hawk final_score:84. strategy: started_high_inf_nation. r1:itr↑6 spd↓25 prt_stop. r2-3:gdp↓ unemp↑ accepted_pain. r4:inf<5 cur_recovered. r5-7:itr↓_gradual gdp_rebound mood_recovery. key:acted_decisively_early.",
        "metadata": {"type": "hof", "layer": 5}
    },
    {
        "layer": 5,
        "chunk_key": "hof.debt_architect_r7",
        "content": "hof:rank4 archetype:debt_architect final_score:79. strategy: r1-4:dbt↑80 used_leverage_for_spd↑50+rnd↑12. inn↑ gdp↑5 paid_off. r5:ctx↑35_revenue swf_liquidation_partial. r6-7:dbt↓70 gdp_sustained. risky_but_calculated.",
        "metadata": {"type": "hof", "layer": 5}
    },
    {
        "layer": 5,
        "chunk_key": "hof.isolationist_r7",
        "content": "hof:rank5 archetype:isolationist final_score:74. strategy: tar↑30+fln=0+wfr=0 throughout. stable_but_slow. gdp_capped_by_no_trade_growth. mood_high from_stability. inn_moderate. safe_floor_strategy never_crisis_never_top.",
        "metadata": {"type": "hof", "layer": 5}
    },
]