from dataclasses import dataclass
from datetime import date

from alembic_utils.pg_trigger import PGTrigger
from sqlalchemy import REAL, Column, Date, ForeignKey, Integer, String

from app.models.base import Base, BaseMixin


class FBrefTeams(Base, BaseMixin):
    __tablename__ = "teams"
    __table_args__ = ({"schema": "fbref"},)

    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    country: str = Column(String)
    league_name: str = Column(String)
    league_url: str = Column(String)

    @staticmethod
    def trg_refresh_updated_at():
        return PGTrigger(
            schema="fbref",
            signature="trg_teams_refresh_updated_at",
            on_entity="fbref.teams",
            definition="""
            BEFORE UPDATE ON fbref.teams
            FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()
            """,
        )


@dataclass
class FBrefPlayers(Base, BaseMixin):
    __tablename__ = "players"
    __table_args__ = ({"schema": "fbref"},)

    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    full_name: str = Column(String)
    dob: date = Column(Date)
    country: str = Column(String)
    team_id: str = Column(String, ForeignKey("fbref.teams.id"))
    position: str = Column(String)

    @staticmethod
    def trg_refresh_updated_at():
        return PGTrigger(
            schema="fbref",
            signature="trg_players_refresh_updated_at",
            on_entity="fbref.players",
            definition="""
            BEFORE UPDATE ON fbref.players
            FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()
            """,
        )


@dataclass
class FBrefScoutingReports(Base, BaseMixin):
    __tablename__ = "scouting_reports"
    __table_args__ = ({"schema": "fbref"},)

    player_id: str = Column(String, ForeignKey("fbref.players.id"), primary_key=True)
    minutes_played: int = Column(Integer)
    goals: float = Column(REAL)
    assists: float = Column(REAL)
    goals_plus_assists: float = Column(REAL)
    non_penalty_goals: float = Column(REAL)
    penalty_kicks_made: float = Column(REAL)
    penalty_kicks_attempted: float = Column(REAL)
    yellow_cards: float = Column(REAL)
    red_cards: float = Column(REAL)
    xg_expected_goals: float = Column(REAL)
    npxg_non_penalty_xg: float = Column(REAL)
    xag_expected_assisted_goals: float = Column(REAL)
    npxg_plus_xag: float = Column(REAL)
    progressive_carries: float = Column(REAL)
    progressive_passes: float = Column(REAL)
    progressive_passes_rec: float = Column(REAL)
    shots_total: float = Column(REAL)
    shots_on_target: float = Column(REAL)
    shots_on_target_pct: float = Column(REAL)
    goals_per_shot: float = Column(REAL)
    goals_per_shot_on_target: float = Column(REAL)
    average_shot_distance: float = Column(REAL)
    shots_from_free_kicks: float = Column(REAL)
    npxg_per_shot: float = Column(REAL)
    goals_xg: float = Column(REAL)
    non_penalty_goals_npxg: float = Column(REAL)
    passes_completed: float = Column(REAL)
    passes_attempted: float = Column(REAL)
    pass_completion_pct: float = Column(REAL)
    total_passing_distance: float = Column(REAL)
    progressive_passing_distance: float = Column(REAL)
    passes_completed_short: float = Column(REAL)
    passes_attempted_short: float = Column(REAL)
    pass_completion_pct_short: float = Column(REAL)
    passes_completed_medium: float = Column(REAL)
    passes_attempted_medium: float = Column(REAL)
    pass_completion_pct_medium: float = Column(REAL)
    passes_completed_long: float = Column(REAL)
    passes_attempted_long: float = Column(REAL)
    pass_completion_pct_long: float = Column(REAL)
    xa_expected_assists: float = Column(REAL)
    key_passes: float = Column(REAL)
    passes_into_final_third: float = Column(REAL)
    passes_into_penalty_area: float = Column(REAL)
    crosses_into_penalty_area: float = Column(REAL)
    live_ball_passes: float = Column(REAL)
    dead_ball_passes: float = Column(REAL)
    passes_from_free_kicks: float = Column(REAL)
    through_balls: float = Column(REAL)
    switches: float = Column(REAL)
    crosses: float = Column(REAL)
    throw_ins_taken: float = Column(REAL)
    corner_kicks: float = Column(REAL)
    inswinging_corner_kicks: float = Column(REAL)
    outswinging_corner_kicks: float = Column(REAL)
    straight_corner_kicks: float = Column(REAL)
    passes_offside: float = Column(REAL)
    passes_blocked: float = Column(REAL)
    shot_creating_actions: float = Column(REAL)
    sca_live_ball_pass: float = Column(REAL)
    sca_dead_ball_pass: float = Column(REAL)
    sca_take_on: float = Column(REAL)
    sca_shot: float = Column(REAL)
    sca_fouls_drawn: float = Column(REAL)
    sca_defensive_action: float = Column(REAL)
    goal_creating_actions: float = Column(REAL)
    gca_live_ball_pass: float = Column(REAL)
    gca_dead_ball_pass: float = Column(REAL)
    gca_take_on: float = Column(REAL)
    gca_shot: float = Column(REAL)
    gca_fouls_drawn: float = Column(REAL)
    gca_defensive_action: float = Column(REAL)
    tackles: float = Column(REAL)
    tackles_won: float = Column(REAL)
    tackles_def_3rd: float = Column(REAL)
    tackles_mid_3rd: float = Column(REAL)
    tackles_att_3rd: float = Column(REAL)
    dribblers_tackled: float = Column(REAL)
    dribbles_challenged: float = Column(REAL)
    pct_of_dribblers_tackled: float = Column(REAL)
    challenges_lost: float = Column(REAL)
    blocks: float = Column(REAL)
    shots_blocked: float = Column(REAL)
    interceptions: float = Column(REAL)
    tkl_plus_int: float = Column(REAL)
    clearances: float = Column(REAL)
    errors: float = Column(REAL)
    touches: float = Column(REAL)
    touches_def_pen: float = Column(REAL)
    touches_def_3rd: float = Column(REAL)
    touches_mid_3rd: float = Column(REAL)
    touches_att_3rd: float = Column(REAL)
    touches_att_pen: float = Column(REAL)
    touches_live_ball: float = Column(REAL)
    take_ons_attempted: float = Column(REAL)
    successful_take_ons: float = Column(REAL)
    successful_take_on_pct: float = Column(REAL)
    times_tackled_during_take_on: float = Column(REAL)
    tackled_during_take_on_pct: float = Column(REAL)
    carries: float = Column(REAL)
    total_carrying_distance: float = Column(REAL)
    progressive_carrying_distance: float = Column(REAL)
    carries_into_final_third: float = Column(REAL)
    carries_into_penalty_area: float = Column(REAL)
    miscontrols: float = Column(REAL)
    dispossessed: float = Column(REAL)
    passes_received: float = Column(REAL)
    second_yellow_card: float = Column(REAL)
    fouls_committed: float = Column(REAL)
    fouls_drawn: float = Column(REAL)
    offsides: float = Column(REAL)
    penalty_kicks_won: float = Column(REAL)
    penalty_kicks_conceded: float = Column(REAL)
    own_goals: float = Column(REAL)
    ball_recoveries: float = Column(REAL)
    aerials_won: float = Column(REAL)
    aerials_lost: float = Column(REAL)
    pct_of_aerials_won: float = Column(REAL)

    @staticmethod
    def trg_refresh_updated_at():
        return PGTrigger(
            schema="fbref",
            signature="trg_scouting_reports_refresh_updated_at",
            on_entity="fbref.scouting_reports",
            definition="""
            BEFORE UPDATE ON fbref.scouting_reports
            FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()
            """,
        )
