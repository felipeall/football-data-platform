"""Register trg_players_refresh_updated_at

Revision ID: 056997eecb1f
Revises: 51fdb7bc49dd
Create Date: 2024-02-04 15:45:15.440572

"""

from typing import Sequence, Union

from alembic_utils.pg_trigger import PGTrigger

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "056997eecb1f"
down_revision: Union[str, None] = "51fdb7bc49dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sofascore_players_trg_players_refresh_updated_at = PGTrigger(
        schema="sofascore",
        signature="trg_players_refresh_updated_at",
        on_entity="sofascore.players",
        is_constraint=False,
        definition="BEFORE UPDATE ON sofascore.players FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()",
    )
    op.create_entity(sofascore_players_trg_players_refresh_updated_at)


def downgrade() -> None:
    sofascore_players_trg_players_refresh_updated_at = PGTrigger(
        schema="sofascore",
        signature="trg_players_refresh_updated_at",
        on_entity="sofascore.players",
        is_constraint=False,
        definition="BEFORE UPDATE ON sofascore.players FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()",
    )
    op.drop_entity(sofascore_players_trg_players_refresh_updated_at)
