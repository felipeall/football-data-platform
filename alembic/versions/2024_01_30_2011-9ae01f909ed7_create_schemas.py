"""Create schemas

Revision ID: 9ae01f909ed7
Revises:
Create Date: 2024-01-30 20:11:48.619852

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9ae01f909ed7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("create schema fbref")
    op.execute("create schema sofascore")
    op.execute("create schema transfermarkt")


def downgrade() -> None:
    op.execute("drop schema fbref")
    op.execute("drop schema sofascore")
    op.execute("drop schema transfermarkt")
