# Layer 2 — Dangerous input combinations
# 20 chunks — pairwise interactions the model must understand

LAYER2 = [
    {
        "layer": 2,
        "chunk_key": "pair.itr_low_spd_high",
        "content": "pair:itr↓+spd↑ stimulus_stack. gdp↑↑ short unemp↓. inf_risk↑↑ monitor inf>8 threshold. hist:2020_covid_response. warn:exit_strategy_needed_r3_or_inf_spirals.",
        "metadata": {"pair": "itr_spd", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.prt_tar_high",
        "content": "pair:prt+tar↑ stagflation_trap. inf↑ from_prt AND trd↓ from_retaliation simultaneously. no_clean_exit_exists. hist:1970s_oil_shock. warn:most_dangerous_combo avoid.",
        "metadata": {"pair": "prt_tar", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.ctx_zero_spd_high",
        "content": "pair:ctx<5+spd>60 revenue_gap. rev↓↓ dbt↑ each_round. forced_choice: raise_ctx OR cut_spd OR prt. prt_temptation_high warn:inf_follows. dbt>80_in_2-3r if_unchanged.",
        "metadata": {"pair": "ctx_spd", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.itr_high_dbt_high",
        "content": "pair:itr>10+dbt>70 debt_service_crisis. interest_payments↑ each_round dbt_compounds. forces_spd↓ OR prt. spd↓→unemp↑ mood↓. prt→inf↑ cur↓. no_good_option only_least_bad.",
        "metadata": {"pair": "itr_dbt", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.rnd_high_spd_low",
        "content": "pair:rnd>12+spd<20 innovation_vacuum. rnd_spend exists but no_infrastructure_to_convert. inn↑_slow or_stagnant. sal_unaffected. waste_of_rnd_budget. fix:spd↑_first then_rnd.",
        "metadata": {"pair": "rnd_spd", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.tar_high_fln_high",
        "content": "pair:tar>40+fln>30 contradiction. tar_signals_protectionism. fln_creates_dependency. partners_may_retaliate_AND_call_loans. cur_double_risk. pick_one_strategy not_both.",
        "metadata": {"pair": "tar_fln", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.prt_itr_low",
        "content": "pair:prt+itr<1 hyperinflation_accelerant. money_supply↑ AND cost_of_holding_cash=0. velocity_of_money↑↑ inf↑↑↑. no_brake_mechanism. hist:weimar_zimbabwe_pattern. critical_warning.",
        "metadata": {"pair": "prt_itr", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.wfr_max_dbt_high",
        "content": "pair:wfr>80+dbt>70 no_safety_net. if_wfr_underperforms swf↓ AND dbt_service_pressure. double_vulnerability. swf_loss forces_emergency_spd_cut OR prt. lower_wfr_first.",
        "metadata": {"pair": "wfr_dbt", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.ctx_high_inn_low",
        "content": "pair:ctx>65+inn<40 capital_flight_risk. high_tax+low_competitiveness→businesses_leave. gdp↓ trd↓ compounds. fix:rnd↑ first_to_raise_inn then_ctx_becomes_defensible.",
        "metadata": {"pair": "ctx_inn", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.spd_high_inf_high",
        "content": "pair:spd>70+inf>10 demand_overload. gov_spending_adding_demand when_supply_already_strained. inf↑↑. must_cut_spd even_though_mood↓. itr↑ alone_insufficient when_fiscal_also_loose.",
        "metadata": {"pair": "spd_inf", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.tar_high_inf_high",
        "content": "pair:tar>40+inf>12 import_cost_spiral. tariffs_raise_import_prices AND inflation_already_high. inf_compounds from_both_sides. cur↓ makes_imports_more_expensive_further. tar↓ counterintuitive_but_needed.",
        "metadata": {"pair": "tar_inf", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.itr_high_unemp_high",
        "content": "pair:itr>12+unemp>12 double_contraction. itr_suppresses_investment AND unemp_suppresses_demand. gdp↓↓ mood↓↓. classic_austerity_trap. spd_targeted_at_employment needed not_broad_cuts.",
        "metadata": {"pair": "itr_unemp", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.fln_high_cur_weak",
        "content": "pair:fln>30+cur<85 repayment_risk. foreign_loans_denominated_in_reserve_currency. cur↓→repayment_cost↑ in_local_terms. dbt_real↑ even_without_new_borrowing. reduce_fln urgently.",
        "metadata": {"pair": "fln_cur", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.rnd_high_inn_plateau",
        "content": "pair:rnd>15+inn>85 diminishing_returns. inn near_ceiling rnd_investment_wasted. redirect_rnd_budget to spd or swf. inn_pts already_converting_to_gdp_bonus no_need_to_push_further.",
        "metadata": {"pair": "rnd_inn", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.spd_low_unemp_high",
        "content": "pair:spd<20+unemp>12 fiscal_austerity_trap. low_spending_reduces_public_jobs AND private_investment. unemp_self_reinforcing mood↓ gdp↓ tax_rev↓. targeted_spd↑ in_employment_programs breaks_cycle.",
        "metadata": {"pair": "spd_unemp", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.prt_mood_trap",
        "content": "pair:prt+mood<40 populist_trap. prt boosts nominal_sal mood↑ short 1r. then inf↑ sal_real↓ mood↓↓ worse_than_before. players_repeat_prt_chasing_mood_boost. each_use_worse_outcome.",
        "metadata": {"pair": "prt_mood", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.swf_low_crisis",
        "content": "pair:swf<50+any_crisis no_buffer. swf=emergency_fund. crisis_without_swf forces_prt OR dbt↑ OR mood_crash. build_swf_in_stable_rounds fln_moderate wfr_moderate.",
        "metadata": {"pair": "swf_crisis", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.ctx_low_inn_high",
        "content": "pair:ctx<15+inn>70 tech_hub_model. low_tax attracts_investment inn_already_high. viable_strategy IF dbt_controlled. risk: rev_gap needs trd_surplus to_compensate. Singapore_analog.",
        "metadata": {"pair": "ctx_inn_positive", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.itr_low_cur_weak",
        "content": "pair:itr<1+cur<85 currency_defense_conflict. itr↓_stimulates_but_weakens_cur further. cur↓→inf↑ imports_expensive. must_choose: defend_cur with itr↑ OR accept_cur_depreciation. cannot_do_both.",
        "metadata": {"pair": "itr_cur", "layer": 2}
    },
    {
        "layer": 2,
        "chunk_key": "pair.spd_high_dbt_high",
        "content": "pair:spd>65+dbt>75 fiscal_cliff. spending_adding_to_debt that_is_already_dangerous. each_round dbt_compounds. markets_demand_itr↑ which_raises_debt_service. spd_must_fall_even_if_painful.",
        "metadata": {"pair": "spd_dbt", "layer": 2}
    },
]