"""Create refresh_updated_at function

Revision ID: 8a0fd60cefcf
Revises: 2a57bf011dbc
Create Date: 2023-08-08 16:52:30.840724

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8a0fd60cefcf"
down_revision: Union[str, None] = "2a57bf011dbc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

create_refresh_updated_at_func = """
    CREATE FUNCTION {schema}.refresh_updated_at()
    RETURNS TRIGGER
    LANGUAGE plpgsql AS
    $func$
    BEGIN
       NEW.updated_at := now();
       RETURN NEW;
    END
    $func$;
    """


def upgrade() -> None:
    op.execute(sa.text(create_refresh_updated_at_func.format(schema="fbref")))
    op.execute(sa.text(create_refresh_updated_at_func.format(schema="sofascore")))
    op.execute(sa.text(create_refresh_updated_at_func.format(schema="tfmkt")))


def downgrade() -> None:
    op.execute(sa.text("DROP FUNCTION fbref.refresh_updated_at() CASCADE"))
    op.execute(sa.text("DROP FUNCTION sofascore.refresh_updated_at() CASCADE"))
    op.execute(sa.text("DROP FUNCTION tfmkt.refresh_updated_at() CASCADE"))
