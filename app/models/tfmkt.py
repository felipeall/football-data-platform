from dataclasses import dataclass
from datetime import date

from sqlalchemy import Column, Date, Integer, String, UniqueConstraint

from app.models.base import AuditMixin, Base, IDMixin


@dataclass
class TfmktMarketValue(Base, IDMixin, AuditMixin):
    __tablename__ = "market_value"
    __table_args__ = (
        UniqueConstraint("player_id", "date"),
        {"schema": "tfmkt"},
    )

    player_id: str = Column(String, nullable=False)
    club_id: str = Column(String, nullable=False)
    date: date = Column(Date, nullable=False)
    market_value: int = Column(Integer, nullable=False)
