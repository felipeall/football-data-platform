"""Create model FBrefPlayers

Revision ID: b58732f1bef8
Revises: 68f8434755eb
Create Date: 2024-01-30 22:19:37.940075

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b58732f1bef8"
down_revision: Union[str, None] = "68f8434755eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "players",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("team_id", sa.String(), nullable=True),
        sa.Column("dob", sa.Date(), nullable=True),
        sa.Column("country_code", sa.String(), nullable=True),
        sa.Column("country_name", sa.String(), nullable=True),
        sa.Column("club_url", sa.String(), nullable=True),
        sa.Column("club_name", sa.String(), nullable=True),
        sa.Column("position", sa.String(), nullable=True),
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
        sa.ForeignKeyConstraint(["team_id"], ["fbref.teams.id"], name=op.f("fk_players_team_id_teams")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_players")),
        schema="fbref",
    )


def downgrade() -> None:
    op.drop_table("players", schema="fbref")
