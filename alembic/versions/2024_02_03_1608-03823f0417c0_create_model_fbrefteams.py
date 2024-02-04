"""Create model FBrefTeams

Revision ID: 03823f0417c0
Revises: e55a606b0a8c
Create Date: 2024-02-03 16:08:16.877868

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "03823f0417c0"
down_revision: Union[str, None] = "e55a606b0a8c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "teams",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("league_name", sa.String(), nullable=True),
        sa.Column("league_url", sa.String(), nullable=True),
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
        schema="fbref",
    )
    op.add_column("players", sa.Column("team_id", sa.String(), nullable=True), schema="fbref")
    op.create_foreign_key(
        op.f("fk_players_team_id_teams"),
        "players",
        "teams",
        ["team_id"],
        ["id"],
        source_schema="fbref",
        referent_schema="fbref",
    )
    op.drop_column("players", "club_url", schema="fbref")
    op.drop_column("players", "club_name", schema="fbref")


def downgrade() -> None:
    op.add_column("players", sa.Column("club_name", sa.VARCHAR(), autoincrement=False, nullable=True), schema="fbref")
    op.add_column("players", sa.Column("club_url", sa.VARCHAR(), autoincrement=False, nullable=True), schema="fbref")
    op.drop_constraint(op.f("fk_players_team_id_teams"), "players", schema="fbref", type_="foreignkey")
    op.drop_column("players", "team_id", schema="fbref")
    op.drop_table("teams", schema="fbref")
