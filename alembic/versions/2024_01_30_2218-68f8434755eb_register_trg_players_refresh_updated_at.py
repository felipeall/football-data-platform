"""Register trg_players_refresh_updated_at

Revision ID: 68f8434755eb
Revises: 9cb7b217e4af
Create Date: 2024-01-30 22:18:52.391555

"""

from typing import Sequence, Union

from alembic_utils.pg_trigger import PGTrigger

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "68f8434755eb"
down_revision: Union[str, None] = "9cb7b217e4af"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    fbref_players_trg_players_refresh_updated_at = PGTrigger(
        schema="fbref",
        signature="trg_players_refresh_updated_at",
        on_entity="fbref.players",
        is_constraint=False,
        definition="BEFORE UPDATE ON fbref.players FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()",
    )
    op.create_entity(fbref_players_trg_players_refresh_updated_at)


def downgrade() -> None:
    fbref_players_trg_players_refresh_updated_at = PGTrigger(
        schema="fbref",
        signature="trg_players_refresh_updated_at",
        on_entity="fbref.players",
        is_constraint=False,
        definition="BEFORE UPDATE ON fbref.players FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()",
    )
    op.drop_entity(fbref_players_trg_players_refresh_updated_at)
