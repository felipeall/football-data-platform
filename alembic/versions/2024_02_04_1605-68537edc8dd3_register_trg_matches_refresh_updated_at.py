"""Register trg_matches_refresh_updated_at

Revision ID: 68537edc8dd3
Revises: fd141d460276
Create Date: 2024-02-04 16:05:33.272137

"""

from typing import Sequence, Union

from alembic_utils.pg_trigger import PGTrigger

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "68537edc8dd3"
down_revision: Union[str, None] = "fd141d460276"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sofascore_matches_trg_matches_refresh_updated_at = PGTrigger(
        schema="sofascore",
        signature="trg_matches_refresh_updated_at",
        on_entity="sofascore.matches",
        is_constraint=False,
        definition="BEFORE UPDATE ON sofascore.matches FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()",
    )
    op.create_entity(sofascore_matches_trg_matches_refresh_updated_at)


def downgrade() -> None:
    sofascore_matches_trg_matches_refresh_updated_at = PGTrigger(
        schema="sofascore",
        signature="trg_matches_refresh_updated_at",
        on_entity="sofascore.matches",
        is_constraint=False,
        definition="BEFORE UPDATE ON sofascore.matches FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()",
    )
    op.drop_entity(sofascore_matches_trg_matches_refresh_updated_at)
