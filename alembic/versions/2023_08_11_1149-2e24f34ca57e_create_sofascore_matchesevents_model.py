"""Create Sofascore MatchesEvents model

Revision ID: 2e24f34ca57e
Revises: 1dac0f14e3c9
Create Date: 2023-08-11 11:49:05.693488

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2e24f34ca57e"
down_revision: Union[str, None] = "1dac0f14e3c9"
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
        sa.Column("player_id", sa.String(), nullable=False),
        sa.Column("player_name", sa.String(), nullable=False),
        sa.Column("accurateCross", sa.Integer(), nullable=True),
        sa.Column("accurateKeeperSweeper", sa.Integer(), nullable=True),
        sa.Column("accurateLongBalls", sa.Integer(), nullable=True),
        sa.Column("accuratePass", sa.Integer(), nullable=True),
        sa.Column("aerialLost", sa.Integer(), nullable=True),
        sa.Column("aerialWon", sa.Integer(), nullable=True),
        sa.Column("bigChanceCreated", sa.Integer(), nullable=True),
        sa.Column("bigChanceMissed", sa.Integer(), nullable=True),
        sa.Column("blockedScoringAttempt", sa.Integer(), nullable=True),
        sa.Column("challengeLost", sa.Integer(), nullable=True),
        sa.Column("clearanceOffLine", sa.Integer(), nullable=True),
        sa.Column("dispossessed", sa.Integer(), nullable=True),
        sa.Column("duelLost", sa.Integer(), nullable=True),
        sa.Column("duelWon", sa.Integer(), nullable=True),
        sa.Column("errorLeadToAGoal", sa.Integer(), nullable=True),
        sa.Column("errorLeadToAShot", sa.Integer(), nullable=True),
        sa.Column("expectedAssists", sa.Float(), nullable=True),
        sa.Column("expectedGoals", sa.Float(), nullable=True),
        sa.Column("fouls", sa.Integer(), nullable=True),
        sa.Column("goalAssist", sa.Integer(), nullable=True),
        sa.Column("goals", sa.Integer(), nullable=True),
        sa.Column("goalsPrevented", sa.Float(), nullable=True),
        sa.Column("goodHighClaim", sa.Integer(), nullable=True),
        sa.Column("hitWoodwork", sa.Integer(), nullable=True),
        sa.Column("interceptionWon", sa.Integer(), nullable=True),
        sa.Column("keyPass", sa.Integer(), nullable=True),
        sa.Column("lastManTackle", sa.Integer(), nullable=True),
        sa.Column("minutesPlayed", sa.Integer(), nullable=True),
        sa.Column("onTargetScoringAttempt", sa.Integer(), nullable=True),
        sa.Column("outfielderBlock", sa.Integer(), nullable=True),
        sa.Column("ownGoals", sa.Integer(), nullable=True),
        sa.Column("penaltyConceded", sa.Integer(), nullable=True),
        sa.Column("penaltyMiss", sa.Integer(), nullable=True),
        sa.Column("penaltySave", sa.Integer(), nullable=True),
        sa.Column("penaltyShootoutGoal", sa.Integer(), nullable=True),
        sa.Column("penaltyShootoutMiss", sa.Integer(), nullable=True),
        sa.Column("penaltyShootoutSave", sa.Integer(), nullable=True),
        sa.Column("penaltyWon", sa.Integer(), nullable=True),
        sa.Column("possessionLostCtrl", sa.Integer(), nullable=True),
        sa.Column("punches", sa.Integer(), nullable=True),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("ratingVersions_alternative", sa.Float(), nullable=True),
        sa.Column("ratingVersions_original", sa.Float(), nullable=True),
        sa.Column("savedShotsFromInsideTheBox", sa.Integer(), nullable=True),
        sa.Column("saves", sa.Integer(), nullable=True),
        sa.Column("shotOffTarget", sa.Integer(), nullable=True),
        sa.Column("totalClearance", sa.Integer(), nullable=True),
        sa.Column("totalContest", sa.Integer(), nullable=True),
        sa.Column("totalCross", sa.Integer(), nullable=True),
        sa.Column("totalKeeperSweeper", sa.Integer(), nullable=True),
        sa.Column("totalLongBalls", sa.Integer(), nullable=True),
        sa.Column("totalOffside", sa.Integer(), nullable=True),
        sa.Column("totalPass", sa.Integer(), nullable=True),
        sa.Column("totalTackle", sa.Integer(), nullable=True),
        sa.Column("touches", sa.Integer(), nullable=True),
        sa.Column("wasFouled", sa.Integer(), nullable=True),
        sa.Column("wonContest", sa.Integer(), nullable=True),
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
        sa.UniqueConstraint("match_id", "player_id", name=op.f("uq_matches_events")),
        schema="sofascore",
    )
    op.execute(sa.text(create_trigger.format(schema="sofascore", table="matches_events")))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("matches_events", schema="sofascore")
    # ### end Alembic commands ###
