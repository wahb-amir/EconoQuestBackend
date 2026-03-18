# Layer 1 — Game mechanics
# 25 chunks explaining how each input affects each output in YOUR simulation
# Model reads these to understand EconoQuest rules, not just real economics

LAYER1 = [
    {
        "layer": 1,
        "chunk_key": "mech.ctx",
        "content": "var:ctx corp_tax. ctx↑→bus_inv↓ short gdp↓ rev↑ dbt↓ long. ctx↓→inv↑ gdp↑ rev↓ dbt↑ risk. opt_band:25-40. ctx>65→cap_flight cur↓. ctx<10→rev_gap force_borrow_or_prt.",
        "metadata": {"var": "ctx", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.itr",
        "content": "var:itr int_rate. itr↑→borrow_cost↑ inv↓ unemp↑ gdp↓ inf↓ cur↑. itr↓→cheap_credit gdp↑ unemp↓ inf↑ cur↓. itr<0.5→rate_floor_trap inf_risk↑↑. itr>15→austerity mood↓ unemp↑↑.",
        "metadata": {"var": "itr", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.spd",
        "content": "var:spd pub_spend %gdp. spd↑→gdp↑ multiplier_effect unemp↓ mood↑ dbt↑. spd>75→inf_pressure dbt_spiral_risk. spd<15→services_collapse unemp↑ mood↓. opt_band:25-50.",
        "metadata": {"var": "spd", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.rnd",
        "content": "var:rnd rd_commit %. rnd↑→inn↑ slow 3-4r lag. inn↑→gdp↑ sal↑ long_run. rnd payoff nonlinear: <5% minimal, 8-15% strong, >20% diminishing. needs spd>20 to convert inn→gdp.",
        "metadata": {"var": "rnd", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.fln",
        "content": "var:fln foreign_lending %. fln↑→swf↑ income but geo_exposure↑ cur_volatility↑. fln>40→dependency_risk if partner_defaults cur↓↓. fln=0→safe but swf_growth slow.",
        "metadata": {"var": "fln", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.wfr",
        "content": "var:wfr wealth_fund_risk %. wfr↑→swf_return↑ potential AND swf_loss_risk↑. wfr>70→boom_bust swf volatile. wfr<20→safe_return swf_stable low_yield. swf acts as emergency buffer for dbt.",
        "metadata": {"var": "wfr", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.tar",
        "content": "var:tar tariff %. tar↑→domestic_industry_protect trd_balance↑ short. tar>35→retaliation_risk trd↓ long. tar>60→import_costs↑ inf↑ cur↓. opt_band:5-25 for most nations.",
        "metadata": {"var": "tar", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.prt",
        "content": "var:prt print_currency bool emergency. prt=1→money_supply↑ inf↑↑ cur↓↓ short_term_gdp↑ mood↑ temporary. inf_lag 1-2r then spikes. each_use compounds. prt>3r→hyper_inf_threshold. never_undo_fast.",
        "metadata": {"var": "prt", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.gdp",
        "content": "out:gdp growth %. driven_by: spd_multiplier + inv(ctx) + inn(rnd_lag) + trd_balance - inf_drag - debt_service. gdp<0 two_consecutive_rounds→recession_penalty mood↓↓ unemp↑↑.",
        "metadata": {"var": "gdp", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.inf",
        "content": "out:inf inflation %. rises_from: prt spd>75 itr<1 tar>50. falls_from: itr↑ spd↓ gdp_gap_close. inf>8 erodes sal_real mood↓. inf>20 cur↓↓ trd↓. inf<1 deflation_risk gdp↓ debt_real↑.",
        "metadata": {"var": "inf", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.unemp",
        "content": "out:unemp %. falls_from: spd↑ gdp↑ itr↓ rnd↑_long. rises_from: itr↑ spd↓ gdp<0 ctx>65. unemp>12→mood↓↓ sal↓ gdp_drag. unemp<3→labour_shortage inf↑ sal↑.",
        "metadata": {"var": "unemp", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.dbt",
        "content": "out:dbt debt/gdp %. rises_from: spd>rev ctx_low prt. falls_from: gdp↑ ctx↑ spd↓ swf_liquidation. dbt>80→credit_risk itr forced↑. dbt>100→debt_spiral auto_penalty_each_round. dbt<30→fiscal_space available.",
        "metadata": {"var": "dbt", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.cur",
        "content": "out:cur currency_index. falls_from: prt inf↑ dbt↑ fln_default. rises_from: itr↑ trd↑ inf↓. cur<80→imports_expensive inf↑ second_order. cur<60→crisis_mode mood↓↓ sal_real↓↓.",
        "metadata": {"var": "cur", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.trd",
        "content": "out:trd trade_balance %. trd↑_from: tar_moderate inn↑ cur↓ competitive. trd↓_from: tar↑ retaliation cur↑ inf↑_domestic. trd>5→cur↑ swf↑. trd<-5→cur↓ dbt↑ pressure.",
        "metadata": {"var": "trd", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.inn",
        "content": "out:inn innovation_pts. driven_by rnd with 3-4r lag. inn>80→gdp_bonus +0.5% sal↑ mood↑ trd↑ competitiveness. inn stagnates if spd<20 or gdp<0 for 2r. once lost takes 3r to rebuild.",
        "metadata": {"var": "inn", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.sal",
        "content": "out:sal avg_salary. sal_nominal↑_from: gdp↑ inn↑ unemp↓. sal_real = sal_nominal / inf_factor. prt raises nominal but inf erodes real. sal_real matters for mood and score.",
        "metadata": {"var": "sal", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.mood",
        "content": "out:mood /100 approval. mood↑_from: sal_real↑ unemp↓ spd↑ gdp↑ inf_low. mood↓_from: inf↑ unemp↑ dbt>80 gdp<0 tax↑ sudden. mood<30→instability_penalty. mood<15→game_over_risk.",
        "metadata": {"var": "mood", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.swf",
        "content": "out:swf sovereign_wealth_fund $b. grows_from: fln_return wfr_yield trd_surplus. depletes_from: emergency_spending wfr_loss dbt_service. swf acts as score_multiplier and crisis_buffer. swf<0→bankrupt_flag.",
        "metadata": {"var": "swf", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.score",
        "content": "score = weighted_avg(gdp inn sal mood) * swf_multiplier - dbt_penalty - inf_penalty. late_rounds weighted higher. mood<30 or inf>25 applies hard_penalty. balanced_nations outscore extremes long_run.",
        "metadata": {"var": "score", "layer": 1}
    },
    {
        "layer": 1,
        "chunk_key": "mech.rounds",
        "content": "game:7 rounds each = 1 fiscal year. decisions_compound: r1_choices affect r4_outputs. recovery_takes: inf 3-4r itr_hikes, dbt 4-5r austerity, inn 3r rnd_investment, mood 2r sal_improvement.",
        "metadata": {"var": "rounds", "layer": 1}
    },
]