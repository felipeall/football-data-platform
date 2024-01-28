from dataclasses import dataclass

from sqlalchemy import REAL, Column, Float, Integer, String, UniqueConstraint

from app.models.base import AuditMixin, Base, IDMixin


@dataclass
class FBRefMatchesEvents(Base, IDMixin, AuditMixin):
    __tablename__ = "matches_events"
    __table_args__ = (
        UniqueConstraint("match_id", "team_id", "player_id"),
        {"schema": "fbref"},
    )

    match_id: str = Column(String, nullable=False)
    team_id: str = Column(String, nullable=False)
    player_id: str = Column(String, nullable=False)
    player_name: str = Column(String, nullable=False)
    min: int = Column(Integer, nullable=False)
    performance_gls: int = Column(Integer, nullable=True)
    performance_ast: int = Column(Integer, nullable=True)
    performance_pk: int = Column(Integer, nullable=True)
    performance_pkatt: int = Column(Integer, nullable=True)
    performance_sh: int = Column(Integer, nullable=True)
    performance_sot: int = Column(Integer, nullable=True)
    performance_touches: int = Column(Integer, nullable=True)
    performance_tkl: int = Column(Integer, nullable=True)
    performance_blocks: int = Column(Integer, nullable=True)
    expected_xg: float = Column(Float, nullable=True)
    expected_npxg: float = Column(Float, nullable=True)
    expected_xag: float = Column(Float, nullable=True)
    sca_sca: int = Column(Integer, nullable=True)
    sca_gca: int = Column(Integer, nullable=True)
    passes_cmp: int = Column(Integer, nullable=True)
    passes_att: int = Column(Integer, nullable=True)
    passes_cmp_pct: float = Column(Float, nullable=True)
    passes_prgp: int = Column(Integer, nullable=True)
    total_cmp: int = Column(Integer, nullable=True)
    total_att: int = Column(Integer, nullable=True)
    total_cmp_pct: float = Column(Float, nullable=True)
    total_totdist: int = Column(Integer, nullable=True)
    total_prgdist: int = Column(Integer, nullable=True)
    short_cmp: int = Column(Integer, nullable=True)
    short_att: int = Column(Integer, nullable=True)
    short_cmp_pct: float = Column(Float, nullable=True)
    medium_cmp: int = Column(Integer, nullable=True)
    medium_att: int = Column(Integer, nullable=True)
    medium_cmp_pct: float = Column(Float, nullable=True)
    long_cmp: int = Column(Integer, nullable=True)
    long_att: int = Column(Integer, nullable=True)
    long_cmp_pct: float = Column(Float, nullable=True)
    ast: int = Column(Integer, nullable=True)
    xag: float = Column(Float, nullable=True)
    xa: float = Column(Float, nullable=True)
    kp: int = Column(Integer, nullable=True)
    final_third: int = Column(Integer, nullable=True)
    ppa: int = Column(Integer, nullable=True)
    crspa: int = Column(Integer, nullable=True)
    prgp: int = Column(Integer, nullable=True)
    att: int = Column(Integer, nullable=True)
    pass_types_live: int = Column(Integer, nullable=True)
    pass_types_dead: int = Column(Integer, nullable=True)
    pass_types_fk: int = Column(Integer, nullable=True)
    pass_types_tb: int = Column(Integer, nullable=True)
    pass_types_sw: int = Column(Integer, nullable=True)
    pass_types_crs: int = Column(Integer, nullable=True)
    pass_types_ti: int = Column(Integer, nullable=True)
    pass_types_ck: int = Column(Integer, nullable=True)
    corner_kicks_in: int = Column(Integer, nullable=True)
    corner_kicks_out: int = Column(Integer, nullable=True)
    corner_kicks_str: int = Column(Integer, nullable=True)
    outcomes_cmp: int = Column(Integer, nullable=True)
    outcomes_off: int = Column(Integer, nullable=True)
    outcomes_blocks: int = Column(Integer, nullable=True)
    tackles_tkl: int = Column(Integer, nullable=True)
    tackles_tklw: int = Column(Integer, nullable=True)
    tackles_def_3rd: int = Column(Integer, nullable=True)
    tackles_mid_3rd: int = Column(Integer, nullable=True)
    tackles_att_3rd: int = Column(Integer, nullable=True)
    challenges_tkl: int = Column(Integer, nullable=True)
    challenges_att: int = Column(Integer, nullable=True)
    challenges_tkl_pct: float = Column(Float, nullable=True)
    challenges_lost: int = Column(Integer, nullable=True)
    blocks_blocks: int = Column(Integer, nullable=True)
    blocks_sh: int = Column(Integer, nullable=True)
    blocks_pass: int = Column(Integer, nullable=True)
    intercep: int = Column(Integer, nullable=True)
    tkl_plus_intercep: int = Column(Integer, nullable=True)
    clr: int = Column(Integer, nullable=True)
    err: int = Column(Integer, nullable=True)
    touches_touches: int = Column(Integer, nullable=True)
    touches_def_pen: int = Column(Integer, nullable=True)
    touches_def_3rd: int = Column(Integer, nullable=True)
    touches_mid_3rd: int = Column(Integer, nullable=True)
    touches_att_3rd: int = Column(Integer, nullable=True)
    touches_att_pen: int = Column(Integer, nullable=True)
    touches_live: int = Column(Integer, nullable=True)
    take_ons_att: int = Column(Integer, nullable=True)
    take_ons_succ: int = Column(Integer, nullable=True)
    take_ons_succ_pct: float = Column(Float, nullable=True)
    take_ons_tkld: int = Column(Integer, nullable=True)
    take_ons_tkld_pct: float = Column(Float, nullable=True)
    carries_carries: int = Column(Integer, nullable=True)
    carries_totdist: int = Column(Integer, nullable=True)
    carries_prgdist: int = Column(Integer, nullable=True)
    carries_prgc: int = Column(Integer, nullable=True)
    carries_final_third: int = Column(Integer, nullable=True)
    carries_cpa: int = Column(Integer, nullable=True)
    carries_mis: int = Column(Integer, nullable=True)
    carries_dis: int = Column(Integer, nullable=True)
    receiving_rec: int = Column(Integer, nullable=True)
    receiving_prgr: int = Column(Integer, nullable=True)
    performance_crdy: int = Column(Integer, nullable=True)
    performance_crdr: int = Column(Integer, nullable=True)
    performance_2crdy: int = Column(Integer, nullable=True)
    performance_fls: int = Column(Integer, nullable=True)
    performance_fld: int = Column(Integer, nullable=True)
    performance_off: int = Column(Integer, nullable=True)
    performance_crs: int = Column(Integer, nullable=True)
    performance_intercep: int = Column(Integer, nullable=True)
    performance_tklw: int = Column(Integer, nullable=True)
    performance_pkwon: int = Column(Integer, nullable=True)
    performance_pkcon: int = Column(Integer, nullable=True)
    performance_og: int = Column(Integer, nullable=True)
    performance_recov: int = Column(Integer, nullable=True)
    aerial_duels_won: int = Column(Integer, nullable=True)
    aerial_duels_lost: int = Column(Integer, nullable=True)
    aerial_duels_won_pct: float = Column(Float, nullable=True)


@dataclass
class FBRefScoutingReports(Base, AuditMixin):
    __tablename__ = "scouting_reports"
    __table_args__ = ({"schema": "fbref"},)

    player_id = Column(String, primary_key=True)
    minutes_played = Column(Integer)
    goals = Column(REAL)
    assists = Column(REAL)
    goals_plus_assists = Column(REAL)
    non_penalty_goals = Column(REAL)
    penalty_kicks_made = Column(REAL)
    penalty_kicks_attempted = Column(REAL)
    yellow_cards = Column(REAL)
    red_cards = Column(REAL)
    xg_expected_goals = Column(REAL)
    npxg_non_penalty_xg = Column(REAL)
    xag_expected_assisted_goals = Column(REAL)
    npxg_plus_xag = Column(REAL)
    progressive_carries = Column(REAL)
    progressive_passes = Column(REAL)
    progressive_passes_rec = Column(REAL)
    shots_total = Column(REAL)
    shots_on_target = Column(REAL)
    shots_on_target_pct = Column(REAL)
    goals_per_shot = Column(REAL)
    goals_per_shot_on_target = Column(REAL)
    average_shot_distance = Column(REAL)
    shots_from_free_kicks = Column(REAL)
    npxg_per_shot = Column(REAL)
    goals_xg = Column(REAL)
    non_penalty_goals_npxg = Column(REAL)
    passes_completed = Column(REAL)
    passes_attempted = Column(REAL)
    pass_completion_pct = Column(REAL)
    total_passing_distance = Column(REAL)
    progressive_passing_distance = Column(REAL)
    passes_completed_short = Column(REAL)
    passes_attempted_short = Column(REAL)
    pass_completion_pct_short = Column(REAL)
    passes_completed_medium = Column(REAL)
    passes_attempted_medium = Column(REAL)
    pass_completion_pct_medium = Column(REAL)
    passes_completed_long = Column(REAL)
    passes_attempted_long = Column(REAL)
    pass_completion_pct_long = Column(REAL)
    xa_expected_assists = Column(REAL)
    key_passes = Column(REAL)
    passes_into_final_third = Column(REAL)
    passes_into_penalty_area = Column(REAL)
    crosses_into_penalty_area = Column(REAL)
    live_ball_passes = Column(REAL)
    dead_ball_passes = Column(REAL)
    passes_from_free_kicks = Column(REAL)
    through_balls = Column(REAL)
    switches = Column(REAL)
    crosses = Column(REAL)
    throw_ins_taken = Column(REAL)
    corner_kicks = Column(REAL)
    inswinging_corner_kicks = Column(REAL)
    outswinging_corner_kicks = Column(REAL)
    straight_corner_kicks = Column(REAL)
    passes_offside = Column(REAL)
    passes_blocked = Column(REAL)
    shot_creating_actions = Column(REAL)
    sca_live_ball_pass = Column(REAL)
    sca_dead_ball_pass = Column(REAL)
    sca_take_on = Column(REAL)
    sca_shot = Column(REAL)
    sca_fouls_drawn = Column(REAL)
    sca_defensive_action = Column(REAL)
    goal_creating_actions = Column(REAL)
    gca_live_ball_pass = Column(REAL)
    gca_dead_ball_pass = Column(REAL)
    gca_take_on = Column(REAL)
    gca_shot = Column(REAL)
    gca_fouls_drawn = Column(REAL)
    gca_defensive_action = Column(REAL)
    tackles = Column(REAL)
    tackles_won = Column(REAL)
    tackles_def_3rd = Column(REAL)
    tackles_mid_3rd = Column(REAL)
    tackles_att_3rd = Column(REAL)
    dribblers_tackled = Column(REAL)
    dribbles_challenged = Column(REAL)
    pct_of_dribblers_tackled = Column(REAL)
    challenges_lost = Column(REAL)
    blocks = Column(REAL)
    shots_blocked = Column(REAL)
    interceptions = Column(REAL)
    tkl_plus_int = Column(REAL)
    clearances = Column(REAL)
    errors = Column(REAL)
    touches = Column(REAL)
    touches_def_pen = Column(REAL)
    touches_def_3rd = Column(REAL)
    touches_mid_3rd = Column(REAL)
    touches_att_3rd = Column(REAL)
    touches_att_pen = Column(REAL)
    touches_live_ball = Column(REAL)
    take_ons_attempted = Column(REAL)
    successful_take_ons = Column(REAL)
    successful_take_on_pct = Column(REAL)
    times_tackled_during_take_on = Column(REAL)
    tackled_during_take_on_pct = Column(REAL)
    carries = Column(REAL)
    total_carrying_distance = Column(REAL)
    progressive_carrying_distance = Column(REAL)
    carries_into_final_third = Column(REAL)
    carries_into_penalty_area = Column(REAL)
    miscontrols = Column(REAL)
    dispossessed = Column(REAL)
    passes_received = Column(REAL)
    second_yellow_card = Column(REAL)
    fouls_committed = Column(REAL)
    fouls_drawn = Column(REAL)
    offsides = Column(REAL)
    penalty_kicks_won = Column(REAL)
    penalty_kicks_conceded = Column(REAL)
    own_goals = Column(REAL)
    ball_recoveries = Column(REAL)
    aerials_won = Column(REAL)
    aerials_lost = Column(REAL)
    pct_of_aerials_won = Column(REAL)
