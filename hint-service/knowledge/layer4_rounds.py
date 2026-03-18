# Layer 4 — Round-aware strategy
# 10 chunks — player sends round number, this contextualises the hint

LAYER4 = [
    {
        "layer": 4,
        "chunk_key": "round.early_r1_r2",
        "content": "round:r1-r2 early_game. priorities: rnd↑_now_for_inn_payoff_r5 spd_stable dbt_acceptable_if_gdp↑ swf_build_start. prt_never_worth_it_early sets_bad_baseline. mood_secondary_to_fundamentals.",
        "metadata": {"round_range": "1-2", "layer": 4}
    },
    {
        "layer": 4,
        "chunk_key": "round.early_mid_r3_r4",
        "content": "round:r3-r4 early_mid. inn_investment_paying_off. check: inf<8 dbt<60 mood>50. if_all_ok: rnd_maintain ctx_optimize swf↑. if_crisis_emerging: act_now 3r_recovery_needed. dont_ignore_warnings.",
        "metadata": {"round_range": "3-4", "layer": 4}
    },
    {
        "layer": 4,
        "chunk_key": "round.mid_r5",
        "content": "round:r5 midpoint_assessment. dbt>60_at_r5→crisis_by_r7_likely. inf>10_at_r5→tough_to_fix_in_2r. inn_should_be_>50_if_rnd_invested_early. swf_buffer_critical_now. consolidate_dont_gamble.",
        "metadata": {"round_range": "5", "layer": 4}
    },
    {
        "layer": 4,
        "chunk_key": "round.late_mid_r6",
        "content": "round:r6 final_stretch. mood+sal_real↑_priority for_final_score. unwind_risky_positions: wfr↓ fln↓_if_cur_weak. no_new_long_term_investments_payoff_too_late. stabilise_and_harvest.",
        "metadata": {"round_range": "6", "layer": 4}
    },
    {
        "layer": 4,
        "chunk_key": "round.final_r7",
        "content": "round:r7 final_round. score_locked_end_of_round. maximize: mood sal_real gdp_positive inn_pts. dbt_reduction_secondary_unless_penalty. swf_protect dont_liquidate. prt_catastrophic_this_round.",
        "metadata": {"round_range": "7", "layer": 4}
    },
    {
        "layer": 4,
        "chunk_key": "round.recovery_timing",
        "content": "recovery_timelines: inf_fix=3-4r_itr_hikes. dbt_fix=4-5r_austerity. inn_rebuild=3r_rnd. mood_fix=2r_sal_improvement. unemp_fix=2-3r_stimulus. know_your_round: if_r>4 some_recoveries_impossible.",
        "metadata": {"type": "timing", "layer": 4}
    },
    {
        "layer": 4,
        "chunk_key": "round.early_investment_thesis",
        "content": "thesis:early_investment. r1-r3 pain acceptable for r5-r7 payoff. rnd_invest_now inn_dividend_later. dbt_moderate_ok_if_gdp_growing. score_weighted_late so_early_sacrifice_rational.",
        "metadata": {"type": "strategy", "layer": 4}
    },
    {
        "layer": 4,
        "chunk_key": "round.late_game_optim",
        "content": "late_game_r5plus: stop_new_experiments. execute_known_strategy. defend_gains. one_lever_at_a_time. each_change_takes_1r_to_show. with_2r_left: only_changes_with_immediate_effect matter.",
        "metadata": {"type": "strategy", "layer": 4}
    },
    {
        "layer": 4,
        "chunk_key": "round.crisis_at_r1",
        "content": "crisis_r1: custom_nation_set_bad_starting_conditions. dont_panic. assess:which_metric_most_critical. one_fix_at_a_time. prt_always_wrong_answer_r1. stabilise_first_then_grow.",
        "metadata": {"type": "crisis_early", "layer": 4}
    },
    {
        "layer": 4,
        "chunk_key": "round.crisis_late",
        "content": "crisis_late_r5plus: triage_only. fix_what_affects_score_most: mood>gdp>sal>inf in_final_rounds. accept_losses_elsewhere. perfect_is_enemy_of_good. pick_one_battle.",
        "metadata": {"type": "crisis_late", "layer": 4}
    },
]