"""Register fun_refresh_updated_at

Revision ID: cc8f04377ee9
Revises: 9ae01f909ed7
Create Date: 2024-01-30 20:13:56.748812

"""

from typing import Sequence, Union

from alembic_utils.pg_function import PGFunction

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cc8f04377ee9"
down_revision: Union[str, None] = "9ae01f909ed7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    public_refresh_updated_at = PGFunction(
        schema="public",
        signature="refresh_updated_at()",
        definition="RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = now(); RETURN NEW; END; $$ LANGUAGE plpgsql",
    )
    op.create_entity(public_refresh_updated_at)


def downgrade() -> None:
    public_refresh_updated_at = PGFunction(
        schema="public",
        signature="refresh_updated_at()",
        definition="RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = now(); RETURN NEW; END; $$ LANGUAGE plpgsql",
    )
    op.drop_entity(public_refresh_updated_at)
