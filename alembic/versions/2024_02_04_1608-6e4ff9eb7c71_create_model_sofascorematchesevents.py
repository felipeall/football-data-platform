"""Create model SofascoreMatchesEvents

Revision ID: 6e4ff9eb7c71
Revises: 68537edc8dd3
Create Date: 2024-02-04 16:08:04.710941

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6e4ff9eb7c71"
down_revision: Union[str, None] = "68537edc8dd3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "matches_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("match_id", sa.String(), nullable=False),
        sa.Column("player_id", sa.String(), nullable=False),
        sa.Column("accurate_cross", sa.Integer(), nullable=True),
        sa.Column("accurate_keeper_sweeper", sa.Integer(), nullable=True),
        sa.Column("accurate_long_balls", sa.Integer(), nullable=True),
        sa.Column("accurate_pass", sa.Integer(), nullable=True),
        sa.Column("aerial_lost", sa.Integer(), nullable=True),
        sa.Column("aerial_won", sa.Integer(), nullable=True),
        sa.Column("big_chance_created", sa.Integer(), nullable=True),
        sa.Column("big_chance_missed", sa.Integer(), nullable=True),
        sa.Column("blocked_scoring_attempt", sa.Integer(), nullable=True),
        sa.Column("challenge_lost", sa.Integer(), nullable=True),
        sa.Column("clearance_off_line", sa.Integer(), nullable=True),
        sa.Column("dispossessed", sa.Integer(), nullable=True),
        sa.Column("duel_lost", sa.Integer(), nullable=True),
        sa.Column("duel_won", sa.Integer(), nullable=True),
        sa.Column("error_lead_to_a_goal", sa.Integer(), nullable=True),
        sa.Column("error_lead_to_a_shot", sa.Integer(), nullable=True),
        sa.Column("expected_assists", sa.REAL(), nullable=True),
        sa.Column("expected_goals", sa.REAL(), nullable=True),
        sa.Column("fouls", sa.Integer(), nullable=True),
        sa.Column("goal_assist", sa.Integer(), nullable=True),
        sa.Column("goals", sa.Integer(), nullable=True),
        sa.Column("goals_prevented", sa.REAL(), nullable=True),
        sa.Column("good_high_claim", sa.Integer(), nullable=True),
        sa.Column("hit_woodwork", sa.Integer(), nullable=True),
        sa.Column("interception_won", sa.Integer(), nullable=True),
        sa.Column("key_pass", sa.Integer(), nullable=True),
        sa.Column("last_man_tackle", sa.Integer(), nullable=True),
        sa.Column("minutes_played", sa.Integer(), nullable=True),
        sa.Column("on_target_scoring_attempt", sa.Integer(), nullable=True),
        sa.Column("outfielder_block", sa.Integer(), nullable=True),
        sa.Column("own_goals", sa.Integer(), nullable=True),
        sa.Column("penalty_conceded", sa.Integer(), nullable=True),
        sa.Column("penalty_miss", sa.Integer(), nullable=True),
        sa.Column("penalty_save", sa.Integer(), nullable=True),
        sa.Column("penalty_shootout_goal", sa.Integer(), nullable=True),
        sa.Column("penalty_shootout_miss", sa.Integer(), nullable=True),
        sa.Column("penalty_shootout_save", sa.Integer(), nullable=True),
        sa.Column("penalty_won", sa.Integer(), nullable=True),
        sa.Column("possession_lost_ctrl", sa.Integer(), nullable=True),
        sa.Column("punches", sa.Integer(), nullable=True),
        sa.Column("rating", sa.REAL(), nullable=True),
        sa.Column("rating_versions_alternative", sa.REAL(), nullable=True),
        sa.Column("rating_versions_original", sa.REAL(), nullable=True),
        sa.Column("saved_shots_from_inside_the_box", sa.Integer(), nullable=True),
        sa.Column("saves", sa.Integer(), nullable=True),
        sa.Column("shot_off_target", sa.Integer(), nullable=True),
        sa.Column("total_clearance", sa.Integer(), nullable=True),
        sa.Column("total_contest", sa.Integer(), nullable=True),
        sa.Column("total_cross", sa.Integer(), nullable=True),
        sa.Column("total_keeper_sweeper", sa.Integer(), nullable=True),
        sa.Column("total_long_balls", sa.Integer(), nullable=True),
        sa.Column("total_offside", sa.Integer(), nullable=True),
        sa.Column("total_pass", sa.Integer(), nullable=True),
        sa.Column("total_tackle", sa.Integer(), nullable=True),
        sa.Column("touches", sa.Integer(), nullable=True),
        sa.Column("was_fouled", sa.Integer(), nullable=True),
        sa.Column("won_contest", sa.Integer(), nullable=True),
        sa.Column("scrapped_at", sa.DateTime(timezone=True), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["match_id"],
            ["sofascore.matches.id"],
            name=op.f("fk_matches_events_match_id_matches"),
        ),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["sofascore.players.id"],
            name=op.f("fk_matches_events_player_id_players"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_matches_events")),
        sa.UniqueConstraint("match_id", "player_id", name=op.f("uq_matches_events")),
        schema="sofascore",
    )


def downgrade() -> None:
    op.drop_table("matches_events", schema="sofascore")
