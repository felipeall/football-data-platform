"""Create model SofascoreTeams

Revision ID: 9b2b2e8afafb
Revises: 5c065a80315e
Create Date: 2024-02-04 15:12:42.704697

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9b2b2e8afafb"
down_revision: Union[str, None] = "5c065a80315e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "teams",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("country_code", sa.String(), nullable=True),
        sa.Column("league_id", sa.String(), nullable=True),
        sa.Column("league_name", sa.String(), nullable=True),
        sa.Column("scrapped_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_teams")),
        schema="sofascore",
    )


def downgrade() -> None:
    op.drop_table("teams", schema="sofascore")
