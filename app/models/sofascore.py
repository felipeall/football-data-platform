from dataclasses import dataclass
from datetime import date

from alembic_utils.pg_trigger import PGTrigger
from sqlalchemy import REAL, Boolean, Column, Date, ForeignKey, Integer, String, UniqueConstraint

from app.models.base import Base, BaseMixin, IDMixin


@dataclass
class SofascoreSeasons(Base, BaseMixin):
    __tablename__ = "seasons"
    __table_args__ = ({"schema": "sofascore"},)

    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    tournament_id: str = Column(String)
    year: int = Column(String)

    @staticmethod
    def trg_refresh_updated_at():
        return PGTrigger(
            schema="sofascore",
            signature="trg_seasons_refresh_updated_at",
            on_entity="sofascore.seasons",
            definition="""
                BEFORE UPDATE ON sofascore.seasons
                FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()
                """,
        )


@dataclass
class SofascoreTournaments(Base, BaseMixin):
    __tablename__ = "tournaments"
    __table_args__ = ({"schema": "sofascore"},)

    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    slug: str = Column(String)
    country_name: str = Column(String)
    country_code: str = Column(String)
    has_performance_graph_feature: bool = Column(Boolean)
    has_event_player_statistics: bool = Column(Boolean)

    @staticmethod
    def trg_refresh_updated_at():
        return PGTrigger(
            schema="sofascore",
            signature="trg_tournaments_refresh_updated_at",
            on_entity="sofascore.tournaments",
            definition="""
                BEFORE UPDATE ON sofascore.tournaments
                FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()
                """,
        )


@dataclass
class SofascoreTeams(Base, BaseMixin):
    __tablename__ = "teams"
    __table_args__ = ({"schema": "sofascore"},)

    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    full_name: str = Column(String)
    country: str = Column(String)
    country_code: str = Column(String)
    league_id: str = Column(String)
    league_name: str = Column(String)

    @staticmethod
    def trg_refresh_updated_at():
        return PGTrigger(
            schema="sofascore",
            signature="trg_teams_refresh_updated_at",
            on_entity="sofascore.teams",
            definition="""
                BEFORE UPDATE ON sofascore.teams
                FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()
                """,
        )


@dataclass
class SofascorePlayers(Base, BaseMixin):
    __tablename__ = "players"
    __table_args__ = ({"schema": "sofascore"},)

    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    short_name: str = Column(String)
    team_id: str = Column(String, ForeignKey("sofascore.teams.id"))
    position: str = Column(String)
    jersey_number: str = Column(String)
    height: str = Column(Integer)
    preferred_foot: str = Column(String)
    retired: bool = Column(Boolean)
    country_code: str = Column(String)
    country_name: str = Column(String)
    dob: date = Column(Date)

    @staticmethod
    def trg_refresh_updated_at():
        return PGTrigger(
            schema="sofascore",
            signature="trg_players_refresh_updated_at",
            on_entity="sofascore.players",
            definition="""
                    BEFORE UPDATE ON sofascore.players
                    FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()
                    """,
        )


@dataclass
class SofascoreMatches(Base, BaseMixin):
    __tablename__ = "matches"
    __table_args__ = ({"schema": "sofascore"},)

    id: str = Column(String, primary_key=True)
    date: date = Column(Date)
    tournament_id: str = Column(String)
    season_id: str = Column(String)
    round: str = Column(String)
    status_id: str = Column(String)
    home_team_id: str = Column(String, ForeignKey("sofascore.teams.id"))
    away_team_id: str = Column(String, ForeignKey("sofascore.teams.id"))
    home_score: int = Column(Integer)
    away_score: int = Column(Integer)
    has_players_statistics: bool = Column(Boolean, nullable=False)

    @staticmethod
    def trg_refresh_updated_at():
        return PGTrigger(
            schema="sofascore",
            signature="trg_matches_refresh_updated_at",
            on_entity="sofascore.matches",
            definition="""
                    BEFORE UPDATE ON sofascore.matches
                    FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()
                    """,
        )


@dataclass
class SofascoreMatchesEvents(Base, IDMixin, BaseMixin):
    __tablename__ = "matches_events"
    __table_args__ = (
        UniqueConstraint("match_id", "player_id"),
        {"schema": "sofascore"},
    )

    match_id: str = Column(String, ForeignKey("sofascore.matches.id"), nullable=False)
    player_id: str = Column(String, ForeignKey("sofascore.players.id"), nullable=False)
    has_statistics: bool = Column(Boolean, nullable=False)
    accurate_cross: int = Column(Integer)
    accurate_keeper_sweeper: int = Column(Integer)
    accurate_long_balls: int = Column(Integer)
    accurate_pass: int = Column(Integer)
    aerial_lost: int = Column(Integer)
    aerial_won: int = Column(Integer)
    big_chance_created: int = Column(Integer)
    big_chance_missed: int = Column(Integer)
    blocked_scoring_attempt: int = Column(Integer)
    challenge_lost: int = Column(Integer)
    clearance_off_line: int = Column(Integer)
    dispossessed: int = Column(Integer)
    duel_lost: int = Column(Integer)
    duel_won: int = Column(Integer)
    error_lead_to_a_goal: int = Column(Integer)
    error_lead_to_a_shot: int = Column(Integer)
    expected_assists: float = Column(REAL)
    expected_goals: float = Column(REAL)
    fouls: int = Column(Integer)
    goal_assist: int = Column(Integer)
    goals: int = Column(Integer)
    goals_prevented: float = Column(REAL)
    good_high_claim: int = Column(Integer)
    hit_woodwork: int = Column(Integer)
    interception_won: int = Column(Integer)
    key_pass: int = Column(Integer)
    last_man_tackle: int = Column(Integer)
    minutes_played: int = Column(Integer)
    on_target_scoring_attempt: int = Column(Integer)
    outfielder_block: int = Column(Integer)
    own_goals: int = Column(Integer)
    penalty_conceded: int = Column(Integer)
    penalty_miss: int = Column(Integer)
    penalty_save: int = Column(Integer)
    penalty_shootout_goal: int = Column(Integer)
    penalty_shootout_miss: int = Column(Integer)
    penalty_shootout_save: int = Column(Integer)
    penalty_won: int = Column(Integer)
    possession_lost_ctrl: int = Column(Integer)
    punches: int = Column(Integer)
    rating: float = Column(REAL)
    rating_versions_alternative: float = Column(REAL)
    rating_versions_original: float = Column(REAL)
    saved_shots_from_inside_the_box: int = Column(Integer)
    saves: int = Column(Integer)
    shot_off_target: int = Column(Integer)
    total_clearance: int = Column(Integer)
    total_contest: int = Column(Integer)
    total_cross: int = Column(Integer)
    total_keeper_sweeper: int = Column(Integer)
    total_long_balls: int = Column(Integer)
    total_offside: int = Column(Integer)
    total_pass: int = Column(Integer)
    total_tackle: int = Column(Integer)
    touches: int = Column(Integer)
    was_fouled: int = Column(Integer)
    won_contest: int = Column(Integer)

    @staticmethod
    def trg_refresh_updated_at():
        return PGTrigger(
            schema="sofascore",
            signature="trg_matches_events_refresh_updated_at",
            on_entity="sofascore.matches_events",
            definition="""
                    BEFORE UPDATE ON sofascore.matches_events
                    FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()
                    """,
        )
