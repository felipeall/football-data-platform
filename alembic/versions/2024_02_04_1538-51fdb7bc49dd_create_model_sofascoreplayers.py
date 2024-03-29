"""Create model SofascorePlayers

Revision ID: 51fdb7bc49dd
Revises: e4b04377e715
Create Date: 2024-02-04 15:38:19.592364

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "51fdb7bc49dd"
down_revision: Union[str, None] = "e4b04377e715"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "players",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("short_name", sa.String(), nullable=True),
        sa.Column("team_id", sa.String(), nullable=True),
        sa.Column("position", sa.String(), nullable=True),
        sa.Column("jersey_number", sa.String(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("preferred_foot", sa.String(), nullable=True),
        sa.Column("retired", sa.Boolean(), nullable=True),
        sa.Column("country_code", sa.String(), nullable=True),
        sa.Column("country_name", sa.String(), nullable=True),
        sa.Column("dob", sa.Date(), nullable=True),
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
        sa.ForeignKeyConstraint(["team_id"], ["sofascore.teams.id"], name=op.f("fk_players_team_id_teams")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_players")),
        schema="sofascore",
    )


def downgrade() -> None:
    op.drop_table("players", schema="sofascore")
