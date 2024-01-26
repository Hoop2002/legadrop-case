"""add condition model and case free

Revision ID: 8cf2d7da46ea
Revises: 3dcd8231cb23
Create Date: 2024-01-26 15:16:07.504055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8cf2d7da46ea"
down_revision: Union[str, None] = "3dcd8231cb23"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "conditions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("condition_id", sa.String(), nullable=True),
        sa.Column("price", sa.DECIMAL(), nullable=False),
        sa.Column("time", sa.Time(), nullable=True),
        sa.Column("timer_reboot", sa.Time(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("condition_id"),
    )
    op.create_table(
        "case_conditions",
        sa.Column("condition_id", sa.String(), nullable=True),
        sa.Column("case_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["case_id"],
            ["cases.case_id"],
        ),
        sa.ForeignKeyConstraint(
            ["condition_id"],
            ["conditions.condition_id"],
        ),
    )
    op.add_column(
        "cases",
        sa.Column("case_free", sa.Boolean(), server_default="False", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("cases", "case_free")
    op.drop_table("case_conditions")
    op.drop_table("conditions")
    # ### end Alembic commands ###
