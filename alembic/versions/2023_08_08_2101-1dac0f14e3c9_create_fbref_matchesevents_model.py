"""Create FBRef MatchesEvents model

Revision ID: 1dac0f14e3c9
Revises: ea294198d6e4
Create Date: 2023-08-08 21:01:37.271614

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1dac0f14e3c9"
down_revision: Union[str, None] = "ea294198d6e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

create_trigger = """
    CREATE TRIGGER tr_{table}_updated BEFORE UPDATE ON {schema}.{table}
    FOR EACH ROW EXECUTE PROCEDURE {schema}.refresh_updated_at();
    """


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "matches_events",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("match_id", sa.String(), nullable=False),
        sa.Column("team_id", sa.String(), nullable=False),
        sa.Column("player_id", sa.String(), nullable=False),
        sa.Column("player_name", sa.String(), nullable=False),
        sa.Column("min", sa.Integer(), nullable=False),
        sa.Column("performance_gls", sa.Integer(), nullable=True),
        sa.Column("performance_ast", sa.Integer(), nullable=True),
        sa.Column("performance_pk", sa.Integer(), nullable=True),
        sa.Column("performance_pkatt", sa.Integer(), nullable=True),
        sa.Column("performance_sh", sa.Integer(), nullable=True),
        sa.Column("performance_sot", sa.Integer(), nullable=True),
        sa.Column("performance_touches", sa.Integer(), nullable=True),
        sa.Column("performance_tkl", sa.Integer(), nullable=True),
        sa.Column("performance_blocks", sa.Integer(), nullable=True),
        sa.Column("expected_xg", sa.Float(), nullable=True),
        sa.Column("expected_npxg", sa.Float(), nullable=True),
        sa.Column("expected_xag", sa.Float(), nullable=True),
        sa.Column("sca_sca", sa.Integer(), nullable=True),
        sa.Column("sca_gca", sa.Integer(), nullable=True),
        sa.Column("passes_cmp", sa.Integer(), nullable=True),
        sa.Column("passes_att", sa.Integer(), nullable=True),
        sa.Column("passes_cmp_pct", sa.Float(), nullable=True),
        sa.Column("passes_prgp", sa.Integer(), nullable=True),
        sa.Column("total_cmp", sa.Integer(), nullable=True),
        sa.Column("total_att", sa.Integer(), nullable=True),
        sa.Column("total_cmp_pct", sa.Float(), nullable=True),
        sa.Column("total_totdist", sa.Integer(), nullable=True),
        sa.Column("total_prgdist", sa.Integer(), nullable=True),
        sa.Column("short_cmp", sa.Integer(), nullable=True),
        sa.Column("short_att", sa.Integer(), nullable=True),
        sa.Column("short_cmp_pct", sa.Float(), nullable=True),
        sa.Column("medium_cmp", sa.Integer(), nullable=True),
        sa.Column("medium_att", sa.Integer(), nullable=True),
        sa.Column("medium_cmp_pct", sa.Float(), nullable=True),
        sa.Column("long_cmp", sa.Integer(), nullable=True),
        sa.Column("long_att", sa.Integer(), nullable=True),
        sa.Column("long_cmp_pct", sa.Float(), nullable=True),
        sa.Column("ast", sa.Integer(), nullable=True),
        sa.Column("xag", sa.Float(), nullable=True),
        sa.Column("xa", sa.Float(), nullable=True),
        sa.Column("kp", sa.Integer(), nullable=True),
        sa.Column("final_third", sa.Integer(), nullable=True),
        sa.Column("ppa", sa.Integer(), nullable=True),
        sa.Column("crspa", sa.Integer(), nullable=True),
        sa.Column("prgp", sa.Integer(), nullable=True),
        sa.Column("att", sa.Integer(), nullable=True),
        sa.Column("pass_types_live", sa.Integer(), nullable=True),
        sa.Column("pass_types_dead", sa.Integer(), nullable=True),
        sa.Column("pass_types_fk", sa.Integer(), nullable=True),
        sa.Column("pass_types_tb", sa.Integer(), nullable=True),
        sa.Column("pass_types_sw", sa.Integer(), nullable=True),
        sa.Column("pass_types_crs", sa.Integer(), nullable=True),
        sa.Column("pass_types_ti", sa.Integer(), nullable=True),
        sa.Column("pass_types_ck", sa.Integer(), nullable=True),
        sa.Column("corner_kicks_in", sa.Integer(), nullable=True),
        sa.Column("corner_kicks_out", sa.Integer(), nullable=True),
        sa.Column("corner_kicks_str", sa.Integer(), nullable=True),
        sa.Column("outcomes_cmp", sa.Integer(), nullable=True),
        sa.Column("outcomes_off", sa.Integer(), nullable=True),
        sa.Column("outcomes_blocks", sa.Integer(), nullable=True),
        sa.Column("tackles_tkl", sa.Integer(), nullable=True),
        sa.Column("tackles_tklw", sa.Integer(), nullable=True),
        sa.Column("tackles_def_3rd", sa.Integer(), nullable=True),
        sa.Column("tackles_mid_3rd", sa.Integer(), nullable=True),
        sa.Column("tackles_att_3rd", sa.Integer(), nullable=True),
        sa.Column("challenges_tkl", sa.Integer(), nullable=True),
        sa.Column("challenges_att", sa.Integer(), nullable=True),
        sa.Column("challenges_tkl_pct", sa.Float(), nullable=True),
        sa.Column("challenges_lost", sa.Integer(), nullable=True),
        sa.Column("blocks_blocks", sa.Integer(), nullable=True),
        sa.Column("blocks_sh", sa.Integer(), nullable=True),
        sa.Column("blocks_pass", sa.Integer(), nullable=True),
        sa.Column("intercep", sa.Integer(), nullable=True),
        sa.Column("tkl_plus_intercep", sa.Integer(), nullable=True),
        sa.Column("clr", sa.Integer(), nullable=True),
        sa.Column("err", sa.Integer(), nullable=True),
        sa.Column("touches_touches", sa.Integer(), nullable=True),
        sa.Column("touches_def_pen", sa.Integer(), nullable=True),
        sa.Column("touches_def_3rd", sa.Integer(), nullable=True),
        sa.Column("touches_mid_3rd", sa.Integer(), nullable=True),
        sa.Column("touches_att_3rd", sa.Integer(), nullable=True),
        sa.Column("touches_att_pen", sa.Integer(), nullable=True),
        sa.Column("touches_live", sa.Integer(), nullable=True),
        sa.Column("take_ons_att", sa.Integer(), nullable=True),
        sa.Column("take_ons_succ", sa.Integer(), nullable=True),
        sa.Column("take_ons_succ_pct", sa.Float(), nullable=True),
        sa.Column("take_ons_tkld", sa.Integer(), nullable=True),
        sa.Column("take_ons_tkld_pct", sa.Float(), nullable=True),
        sa.Column("carries_carries", sa.Integer(), nullable=True),
        sa.Column("carries_totdist", sa.Integer(), nullable=True),
        sa.Column("carries_prgdist", sa.Integer(), nullable=True),
        sa.Column("carries_prgc", sa.Integer(), nullable=True),
        sa.Column("carries_final_third", sa.Integer(), nullable=True),
        sa.Column("carries_cpa", sa.Integer(), nullable=True),
        sa.Column("carries_mis", sa.Integer(), nullable=True),
        sa.Column("carries_dis", sa.Integer(), nullable=True),
        sa.Column("receiving_rec", sa.Integer(), nullable=True),
        sa.Column("receiving_prgr", sa.Integer(), nullable=True),
        sa.Column("performance_crdy", sa.Integer(), nullable=True),
        sa.Column("performance_crdr", sa.Integer(), nullable=True),
        sa.Column("performance_2crdy", sa.Integer(), nullable=True),
        sa.Column("performance_fls", sa.Integer(), nullable=True),
        sa.Column("performance_fld", sa.Integer(), nullable=True),
        sa.Column("performance_off", sa.Integer(), nullable=True),
        sa.Column("performance_crs", sa.Integer(), nullable=True),
        sa.Column("performance_intercep", sa.Integer(), nullable=True),
        sa.Column("performance_tklw", sa.Integer(), nullable=True),
        sa.Column("performance_pkwon", sa.Integer(), nullable=True),
        sa.Column("performance_pkcon", sa.Integer(), nullable=True),
        sa.Column("performance_og", sa.Integer(), nullable=True),
        sa.Column("performance_recov", sa.Integer(), nullable=True),
        sa.Column("aerial_duels_won", sa.Integer(), nullable=True),
        sa.Column("aerial_duels_lost", sa.Integer(), nullable=True),
        sa.Column("aerial_duels_won_pct", sa.Float(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_matches_events")),
        sa.UniqueConstraint("match_id", "team_id", "player_id", name=op.f("uq_matches_events")),
        schema="fbref",
    )
    op.execute(sa.text(create_trigger.format(schema="fbref", table="matches_events")))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("matches_events", schema="fbref")
    # ### end Alembic commands ###