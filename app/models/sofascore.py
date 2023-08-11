# ruff: noqa: N815
from dataclasses import dataclass

from sqlalchemy import Column, Float, Integer, String, UniqueConstraint

from app.models.base import AuditMixin, Base, IDMixin


@dataclass
class SofascoreMatchesReports(Base, IDMixin, AuditMixin):
    __tablename__ = "matches_reports"
    __table_args__ = (
        UniqueConstraint("match_id", "player_id"),
        {"schema": "sofascore"},
    )

    match_id: str = Column(String, nullable=False)
    player_id: str = Column(String, nullable=False)
    totalPass: int = Column(Integer, nullable=True)
    accuratePass: int = Column(Integer, nullable=True)
    totalLongBalls: int = Column(Integer, nullable=True)
    accurateLongBalls: int = Column(Integer, nullable=True)
    totalClearance: int = Column(Integer, nullable=True)
    savedShotsFromInsideTheBox: int = Column(Integer, nullable=True)
    saves: int = Column(Integer, nullable=True)
    punches: int = Column(Integer, nullable=True)
    minutesPlayed: int = Column(Integer, nullable=True)
    touches: int = Column(Integer, nullable=True)
    rating: float = Column(Float, nullable=True)
    possessionLostCtrl: int = Column(Integer, nullable=True)
    expectedGoals: float = Column(Float, nullable=True)
    goalsPrevented: float = Column(Float, nullable=True)
    ratingVersions_original: float = Column(Float, nullable=True)
    ratingVersions_alternative: float = Column(Float, nullable=True)
    aerialWon: int = Column(Integer, nullable=True)
    duelLost: int = Column(Integer, nullable=True)
    duelWon: int = Column(Integer, nullable=True)
    challengeLost: int = Column(Integer, nullable=True)
    totalContest: int = Column(Integer, nullable=True)
    onTargetScoringAttempt: int = Column(Integer, nullable=True)
    goals: int = Column(Integer, nullable=True)
    totalTackle: int = Column(Integer, nullable=True)
    keyPass: int = Column(Integer, nullable=True)
    expectedAssists: float = Column(Float, nullable=True)
    aerialLost: int = Column(Integer, nullable=True)
    blockedScoringAttempt: int = Column(Integer, nullable=True)
    outfielderBlock: int = Column(Integer, nullable=True)
    interceptionWon: int = Column(Integer, nullable=True)
    fouls: int = Column(Integer, nullable=True)
    dispossessed: int = Column(Integer, nullable=True)
    wasFouled: int = Column(Integer, nullable=True)
    totalCross: int = Column(Integer, nullable=True)
    wonContest: int = Column(Integer, nullable=True)
    shotOffTarget: int = Column(Integer, nullable=True)
    accurateCross: int = Column(Integer, nullable=True)
    penaltyWon: int = Column(Integer, nullable=True)
    totalOffside: int = Column(Integer, nullable=True)
    bigChanceMissed: int = Column(Integer, nullable=True)
    penaltyMiss: int = Column(Integer, nullable=True)
    penaltyConceded: int = Column(Integer, nullable=True)
    bigChanceCreated: int = Column(Integer, nullable=True)
    goodHighClaim: int = Column(Integer, nullable=True)
    goalAssist: int = Column(Integer, nullable=True)
    totalKeeperSweeper: int = Column(Integer, nullable=True)
    accurateKeeperSweeper: int = Column(Integer, nullable=True)
    hitWoodwork: int = Column(Integer, nullable=True)
    ownGoals: int = Column(Integer, nullable=True)
    errorLeadToAShot: int = Column(Integer, nullable=True)
    lastManTackle: int = Column(Integer, nullable=True)
    clearanceOffLine: int = Column(Integer, nullable=True)
    errorLeadToAGoal: int = Column(Integer, nullable=True)
    penaltySave: int = Column(Integer, nullable=True)
    penaltyShootoutSave: int = Column(Integer, nullable=True)
    penaltyShootoutMiss: int = Column(Integer, nullable=True)
    penaltyShootoutGoal: int = Column(Integer, nullable=True)
