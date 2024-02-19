"""Create model FBrefTeams

Revision ID: 9cb7b217e4af
Revises: cc8f04377ee9
Create Date: 2024-01-30 22:17:57.766854

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9cb7b217e4af"
down_revision: Union[str, None] = "cc8f04377ee9"
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
        schema="fbref",
    )


def downgrade() -> None:
    op.drop_table("teams", schema="fbref")
