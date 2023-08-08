"""Crate Transfermarkt MarketValue model

Revision ID: ea294198d6e4
Revises: 8a0fd60cefcf
Create Date: 2023-08-08 16:54:19.550473

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ea294198d6e4"
down_revision: Union[str, None] = "8a0fd60cefcf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

create_trigger = """
    CREATE TRIGGER tr_{table}_updated BEFORE UPDATE ON {schema}.{table}
    FOR EACH ROW EXECUTE PROCEDURE {schema}.refresh_updated_at();
    """


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "market_value",
        sa.Column("player_id", sa.String(), nullable=False),
        sa.Column("club_id", sa.String(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("market_value", sa.Integer(), nullable=False),
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_market_value")),
        sa.UniqueConstraint("player_id", "date", name=op.f("uq_market_value")),
        schema="tfmkt",
    )
    op.execute(sa.text(create_trigger.format(schema="tfmkt", table="market_value")))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("market_value", schema="tfmkt")
    # ### end Alembic commands ###
