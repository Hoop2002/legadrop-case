"""add promo table

Revision ID: 0396f003ccf4
Revises: 798e3d6084f0
Create Date: 2024-01-23 16:35:09.454541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0396f003ccf4"
down_revision: Union[str, None] = "798e3d6084f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "promo_codes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "type_code",
            postgresql.ENUM("bonus", "balance", name="promo_types"),
            nullable=False,
        ),
        sa.Column("activations", sa.Integer(), nullable=True),
        sa.Column("to_date", sa.DateTime(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("calcs", sa.Column("promo_code_id", sa.Integer(), nullable=False))
    op.create_foreign_key(None, "calcs", "promo_codes", ["promo_code_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "calcs", type_="foreignkey")
    op.drop_column("calcs", "promo_code_id")
    op.drop_table("promo_codes")
    # ### end Alembic commands ###
