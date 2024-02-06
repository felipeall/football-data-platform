"""Register trg_teams_refresh_updated_at

Revision ID: e4b04377e715
Revises: 9b2b2e8afafb
Create Date: 2024-02-04 15:17:33.933840

"""

from typing import Sequence, Union

from alembic_utils.pg_trigger import PGTrigger

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e4b04377e715"
down_revision: Union[str, None] = "9b2b2e8afafb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sofascore_teams_trg_teams_refresh_updated_at = PGTrigger(
        schema="sofascore",
        signature="trg_teams_refresh_updated_at",
        on_entity="sofascore.teams",
        is_constraint=False,
        definition="BEFORE UPDATE ON sofascore.teams FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()",
    )
    op.create_entity(sofascore_teams_trg_teams_refresh_updated_at)


def downgrade() -> None:
    sofascore_teams_trg_teams_refresh_updated_at = PGTrigger(
        schema="sofascore",
        signature="trg_teams_refresh_updated_at",
        on_entity="sofascore.teams",
        is_constraint=False,
        definition="BEFORE UPDATE ON sofascore.teams FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()",
    )
    op.drop_entity(sofascore_teams_trg_teams_refresh_updated_at)
