"""Register trg_scouting_reports_refresh_updated_at

Revision ID: e55a606b0a8c
Revises: b58732f1bef8
Create Date: 2024-01-30 22:20:05.442036

"""

from typing import Sequence, Union

from alembic_utils.pg_trigger import PGTrigger

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e55a606b0a8c"
down_revision: Union[str, None] = "b58732f1bef8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    fbref_scouting_reports_trg_scouting_reports_refresh_updated_at = PGTrigger(
        schema="fbref",
        signature="trg_scouting_reports_refresh_updated_at",
        on_entity="fbref.scouting_reports",
        is_constraint=False,
        definition="BEFORE UPDATE ON fbref.scouting_reports FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()",
    )
    op.create_entity(fbref_scouting_reports_trg_scouting_reports_refresh_updated_at)


def downgrade() -> None:
    fbref_scouting_reports_trg_scouting_reports_refresh_updated_at = PGTrigger(
        schema="fbref",
        signature="trg_scouting_reports_refresh_updated_at",
        on_entity="fbref.scouting_reports",
        is_constraint=False,
        definition="BEFORE UPDATE ON fbref.scouting_reports FOR EACH ROW EXECUTE FUNCTION public.refresh_updated_at()",
    )
    op.drop_entity(fbref_scouting_reports_trg_scouting_reports_refresh_updated_at)
