from dataclasses import dataclass
from datetime import date

from alembic_utils.pg_trigger import PGTrigger
from sqlalchemy import Column, Date, Integer, String, UniqueConstraint

from app.models.base import Base, BaseMixin, IDMixin


@dataclass
class TransfermarktMarketValue(Base, BaseMixin, IDMixin):
    __tablename__ = "market_value"
    __table_args__ = (
        UniqueConstraint("player_id", "date"),
        {"schema": "transfermarkt"},
    )

    player_id: str = Column(String, nullable=False)
    club_id: str = Column(String, nullable=False)
    date: date = Column(Date, nullable=False)
    age: int = Column(Integer, nullable=False)
    value: int = Column(Integer, nullable=False)

    @staticmethod
    def trg_refresh_updated_at():
        return PGTrigger(
            schema="transfermarkt",
            signature="trg_market_value_refresh_updated_at",
            on_entity="transfermarkt.market_value",
            definition="""
                BEFORE UPDATE ON transfermarkt.market_value
                FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()
                """,
        )
