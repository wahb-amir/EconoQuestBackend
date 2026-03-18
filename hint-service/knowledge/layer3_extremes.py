# Layer 3 — Extreme condition playbooks
# 35 chunks — trigger-based, one per dangerous state range

LAYER3 = [
    {
        "layer": 3,
        "chunk_key": "extreme.hyper_inf",
        "content": "cond:hyper_inf trig:inf>20 state:cur↓↓ sal_real↓↓ mood↓↓ trd↓. cause:prt_overuse OR itr<1+spd>75. fix:stop_prt_immediately itr↑_urgent spd↓. warn:gdp_loss_3-5%_unavoidable. recovery:4-6r. hist:weimar_zimbabwe.",
        "metadata": {"trigger": "inf>20", "severity": "critical", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.high_inf",
        "content": "cond:high_inf trig:inf>12 state:sal_real↓ mood↓ cur↓. still_recoverable. fix:itr↑_gradual spd↓_moderate stop_prt_if_active. window:2-3r before_hyper. dont_panic_cut_gdp_too_fast.",
        "metadata": {"trigger": "inf>12", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.zero_tax",
        "content": "cond:zero_tax trig:ctx<5 state:rev_gap_widening dbt↑_each_round. short_term:gdp↑ inv↑ mood↑. long_term:dbt_spiral in_3-4r. fix:ctx↑_gradually 5pts/r to_minimize_inv_shock. avoid_prt_temptation. warn:mood_boost_temporary.",
        "metadata": {"trigger": "ctx<5", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.debt_crisis",
        "content": "cond:debt_crisis trig:dbt>85 state:debt_service>revenue swf_pressure. options:1_swf_liquidation_buys_2-3r 2_spd_structural_cuts 3_ctx↑ 4_gdp_growth_out. avoid_prt:makes_worse cur↓. warn:dbt>100_game_penalty.",
        "metadata": {"trigger": "dbt>85", "severity": "critical", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.debt_spiral",
        "content": "cond:debt_spiral trig:dbt>85+itr>8 state:compound_interest_exceeds_gdp_growth each_round_worse. only_exit:gdp_growth_surge OR swf_liquidation_then_structural_reform. prt_makes_cur↓_accelerates_spiral.",
        "metadata": {"trigger": "dbt>85+itr>8", "severity": "critical", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.stagflation",
        "content": "cond:stagflation trig:inf>10+unemp>10 state:classic_policy_dilemma. itr↑_kills_unemp_worse. spd↓_kills_gdp_worse. no_clean_lever. best:rnd↑_long_play supply_side_fix tar↓_reduce_import_costs itr_small↑_only.",
        "metadata": {"trigger": "inf>10+unemp>10", "severity": "critical", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.cur_collapse",
        "content": "cond:cur_collapse trig:cur<70 state:imports_expensive inf↑ trd_deficit_widens fln_repayment↑. fix:itr↑_to_defend_cur fln↓_reduce_exposure tar_moderate_not_max. warn:tar↑↑_risks_retaliation trd_worsens.",
        "metadata": {"trigger": "cur<70", "severity": "critical", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.cur_weak",
        "content": "cond:cur_weak trig:cur<85 state:import_costs_rising inf_pressure. act_now_before_collapse. itr_small↑ prt_stop swf_can_defend_cur short_term. trd↑_competitive_exports_help.",
        "metadata": {"trigger": "cur<85", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.recession",
        "content": "cond:recession trig:gdp<-2 state:unemp↑↑ mood↓↓ tax_rev↓ dbt↑. keynesian_response: spd↑ itr↓. BUT if_inf>8 cannot_use_both_levers. if_dbt>70 cannot_afford_spd↑. assess_constraints_first.",
        "metadata": {"trigger": "gdp<-2", "severity": "critical", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.contraction",
        "content": "cond:contraction trig:gdp<0 state:early_warning not_yet_recession. act_early: itr_small↓ OR spd_targeted↑_employment. check_inf_first if_inf<6 safe_to_stimulate. rnd↑_now_pays_in_2r.",
        "metadata": {"trigger": "gdp<0", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.mood_collapse",
        "content": "cond:mood_collapse trig:mood<30 state:instability_penalty_active. cause:inf↑ OR unemp↑ OR gdp<0 prolonged. quick_fix:spd↑_visible_services prt_NOT_recommended_only_delays. structural:sal_real↑ through_inf↓+gdp↑.",
        "metadata": {"trigger": "mood<30", "severity": "critical", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.mood_low",
        "content": "cond:mood_low trig:mood<45 state:approval_declining. check_cause: unemp? sal_real? inf? address_root_not_symptom. spd↑_on_services_buys_1-2r. long_fix:gdp↑+inf↓+unemp↓.",
        "metadata": {"trigger": "mood<45", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.swf_depleted",
        "content": "cond:swf_depleted trig:swf<50 state:no_emergency_buffer crisis_vulnerability↑. rebuild_priority: fln_moderate wfr_moderate trd_surplus. do_not_liquidate_swf_for_short_term_mood. swf=insurance.",
        "metadata": {"trigger": "swf<50", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.swf_bankrupt",
        "content": "cond:swf_bankrupt trig:swf<0 state:sovereign_default_risk score_penalty. emergency: ctx↑ spd↓ fln↑_carefully prt_avoided. game_ending_risk if_dbt_also>90.",
        "metadata": {"trigger": "swf<0", "severity": "critical", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.unemp_crisis",
        "content": "cond:unemp_crisis trig:unemp>15 state:mood↓↓ sal↓ gdp_drag tax_rev↓. cause:itr>12 OR spd<20 OR gdp<0_prolonged. fix:spd↑_employment_programs itr↓_if_inf<6. warn:unemp_lags_policy_by_1-2r.",
        "metadata": {"trigger": "unemp>15", "severity": "critical", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.unemp_high",
        "content": "cond:unemp_high trig:unemp>10 state:mood↓ gdp_subdued. act_before_crisis: targeted_spd↑ rnd↑_creates_jobs_long. itr↓_if_inf_allows. dont_wait_unemp_compounds.",
        "metadata": {"trigger": "unemp>10", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.prt_chain",
        "content": "cond:prt_chain trig:prt_used>2r_consecutively state:inf_compounding cur↓_each_r sal_real↓. cannot_stop_suddenly withdrawal_causes_gdp_dip. taper:prt_off itr↑_gradual spd↓_moderate. 4-6r_stabilise.",
        "metadata": {"trigger": "prt_consecutive", "severity": "critical", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.trd_deficit_severe",
        "content": "cond:trd_deficit trig:trd<-5 state:cur↓_pressure dbt↑ swf↓. fix:tar_moderate(not_max) inn↑_competitiveness cur↓_makes_exports_cheaper. warn:tar↑↑_triggers_retaliation worsens_trd.",
        "metadata": {"trigger": "trd<-5", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.inn_stagnant",
        "content": "cond:inn_stagnant trig:inn<30+r>4 state:gdp_ceiling_approaching sal_growth_limited trd_uncompetitive. cause:rnd<5 OR spd<20 OR gdp<0_prolonged. fix:rnd↑_now 3r_lag_to_payoff spd↑_base.",
        "metadata": {"trigger": "inn<30+r>4", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.deflation",
        "content": "cond:deflation trig:inf<1 state:debt_real↑ gdp↓_risk consumer_spending↓. cause:itr>15 OR spd<15. fix:itr↓ spd↑_targeted. warn:deflation_trap_hard_to_exit once_entrenched. hist:japan_1990s.",
        "metadata": {"trigger": "inf<1", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.cap_flight",
        "content": "cond:cap_flight trig:ctx>65+inn<50 state:businesses_leaving gdp↓ trd↓ unemp↑. fix:ctx↓_gradual rnd↑_inn↑ first_make_competitive_then_tax. warn:sudden_ctx↑_triggers_flight too.",
        "metadata": {"trigger": "ctx>65+inn<50", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.labour_shortage",
        "content": "cond:labour_shortage trig:unemp<3 state:sal↑↑ inf_pressure wage_spiral. cause:too_much_stimulus. fix:itr_small↑ spd_stable rnd↑_productivity_offset. warn:fighting_success_paradox.",
        "metadata": {"trigger": "unemp<3", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.protectionism_trap",
        "content": "cond:protectionism_trap trig:tar>60 state:retaliation_active trd↓↓ import_costs↑ inf↑. trapped: tar↓_helps_long_but_domestic_industry_exposed. gradual_tar↓ over_2-3r with_inn↑_to_compensate.",
        "metadata": {"trigger": "tar>60", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.wfr_bust",
        "content": "cond:wfr_bust trig:wfr>80+swf↓_this_round state:fund_underperformed swf_loss. immediate:wfr↓_to_50 accept_lower_return. if_dbt>70 also: emergency_mode no_more_risk. stability_over_returns.",
        "metadata": {"trigger": "wfr>80+swf_down", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.geo_exposure",
        "content": "cond:geo_exposure trig:fln>50 state:partner_default_risk cur_volatility↑. diversify: fln↓_gradually wfr↓_reduce_double_risk. if_cur<90 also: fln_repayment_costs_rising urgently_reduce.",
        "metadata": {"trigger": "fln>50", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.fiscal_cliff",
        "content": "cond:fiscal_cliff trig:dbt>75+spd>65 state:adding_to_unsustainable_debt each_round. markets_demand_itr↑_which_compounds_dbt. must_cut_spd 10pts/r even_if_gdp↓ short. no_alternative.",
        "metadata": {"trigger": "dbt>75+spd>65", "severity": "critical", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.balanced_risk",
        "content": "cond:balanced trig:all_metrics_normal state:optimization_phase not_crisis_management. focus:inn↑_rnd competitive_advantage trd_surplus swf_build wfr_moderate_returns. leaderboard_play.",
        "metadata": {"trigger": "all_normal", "severity": "info", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.overheating",
        "content": "cond:overheating trig:gdp>6+inf>8 state:growth_too_fast inf_catching_up. itr_small↑ spd_stable rnd_maintained. controlled_landing_better_than_crash. dont_kill_gdp_just_cool_it.",
        "metadata": {"trigger": "gdp>6+inf>8", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.debt_moderate",
        "content": "cond:debt_moderate trig:dbt>65 state:manageable_but_watch. gdp_growth_reduces_ratio naturally. avoid_spd↑ and_prt. ctx_stable_revenue. itr_moderate. act_before_dbt>80.",
        "metadata": {"trigger": "dbt>65", "severity": "info", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.sal_real_crisis",
        "content": "cond:sal_real_crisis trig:sal↑_nominal+inf>12 state:workers_poorer_despite_raises mood↓ unemp↑_pressure. inf_erasing_gains. must_reduce_inf not_raise_nominal_sal_further. itr↑ spd↓.",
        "metadata": {"trigger": "sal_nominal_up+inf>12", "severity": "warning", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.inn_boom",
        "content": "cond:inn_boom trig:inn>80 state:gdp_bonus_active trd↑_competitive sal↑. maintain:rnd>8 spd>25. now_focus_on: dbt_reduction swf_build mood_consolidation. dont_cut_rnd_to_zero harvest_carefully.",
        "metadata": {"trigger": "inn>80", "severity": "info", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.currency_surplus",
        "content": "cond:cur_surplus trig:cur>130 state:exports_expensive trd↓_risk competitive_loss. cause:itr_too_high or_trd_surplus_large. itr_small↓ fln↑_moderate tar↓ to_rebalance.",
        "metadata": {"trigger": "cur>130", "severity": "info", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.swf_rich",
        "content": "cond:swf_rich trig:swf>500 state:strong_buffer available. options:wfr↑_moderate for_returns fln↑_selective spd↑_investment rnd↑. score_multiplier_active. protect_by_avoiding_prt.",
        "metadata": {"trigger": "swf>500", "severity": "info", "layer": 3}
    },
    {
        "layer": 3,
        "chunk_key": "extreme.late_game_crisis",
        "content": "cond:late_crisis trig:r>5+any_critical state:limited_rounds_to_recover. prioritize: mood+sal_real for_score. dbt_reduction secondary_if_mood_ok. accept_gdp_trade for_stability. no_risky_bets.",
        "metadata": {"trigger": "r>5+critical", "severity": "critical", "layer": 3}
    },
]