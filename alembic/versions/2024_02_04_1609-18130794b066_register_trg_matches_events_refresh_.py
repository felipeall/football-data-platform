"""Register trg_matches_events_refresh_updated_at

Revision ID: 18130794b066
Revises: 6e4ff9eb7c71
Create Date: 2024-02-04 16:09:26.495998

"""

from typing import Sequence, Union

from alembic_utils.pg_trigger import PGTrigger

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "18130794b066"
down_revision: Union[str, None] = "6e4ff9eb7c71"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sofascore_matches_events_trg_matches_events_refresh_updated_at = PGTrigger(
        schema="sofascore",
        signature="trg_matches_events_refresh_updated_at",
        on_entity="sofascore.matches_events",
        is_constraint=False,
        definition=(
            "BEFORE UPDATE ON sofascore.matches_events FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()"
        ),
    )
    op.create_entity(sofascore_matches_events_trg_matches_events_refresh_updated_at)


def downgrade() -> None:
    sofascore_matches_events_trg_matches_events_refresh_updated_at = PGTrigger(
        schema="sofascore",
        signature="trg_matches_events_refresh_updated_at",
        on_entity="sofascore.matches_events",
        is_constraint=False,
        definition=(
            "BEFORE UPDATE ON sofascore.matches_events FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()"
        ),
    )
    op.drop_entity(sofascore_matches_events_trg_matches_events_refresh_updated_at)
