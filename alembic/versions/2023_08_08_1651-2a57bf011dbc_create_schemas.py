"""Create schemas

Revision ID: 2a57bf011dbc
Revises:
Create Date: 2023-08-08 16:51:54.424699

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2a57bf011dbc"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("create schema fbref")
    op.execute("create schema sofascore")
    op.execute("create schema tfmkt")


def downgrade() -> None:
    op.execute("drop schema fbref")
    op.execute("drop schema sofascore")
    op.execute("drop schema tfmkt")
