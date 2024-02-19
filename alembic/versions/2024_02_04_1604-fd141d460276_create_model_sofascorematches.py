"""Create model SofascoreMatches

Revision ID: fd141d460276
Revises: 056997eecb1f
Create Date: 2024-02-04 16:04:29.895631

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fd141d460276"
down_revision: Union[str, None] = "056997eecb1f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "matches",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("tournament_id", sa.String(), nullable=True),
        sa.Column("season_id", sa.String(), nullable=True),
        sa.Column("round", sa.String(), nullable=True),
        sa.Column("status_id", sa.String(), nullable=True),
        sa.Column("home_team_id", sa.String(), nullable=True),
        sa.Column("away_team_id", sa.String(), nullable=True),
        sa.Column("home_score", sa.Integer(), nullable=True),
        sa.Column("away_score", sa.Integer(), nullable=True),
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
        sa.ForeignKeyConstraint(["away_team_id"], ["sofascore.teams.id"], name=op.f("fk_matches_away_team_id_teams")),
        sa.ForeignKeyConstraint(["home_team_id"], ["sofascore.teams.id"], name=op.f("fk_matches_home_team_id_teams")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_matches")),
        schema="sofascore",
    )


def downgrade() -> None:
    op.drop_table("matches", schema="sofascore")
