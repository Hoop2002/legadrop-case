"""Fix nullable fields

Revision ID: 27b40b2210a4
Revises: cb6ad08d0e36
Create Date: 2024-01-20 00:34:25.188552

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "27b40b2210a4"
down_revision: Union[str, None] = "cb6ad08d0e36"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "rarity_category", "name", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "rarity_category",
        "category_percent",
        existing_type=sa.NUMERIC(),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "rarity_category", "category_percent", existing_type=sa.NUMERIC(), nullable=True
    )
    op.alter_column(
        "rarity_category", "name", existing_type=sa.VARCHAR(), nullable=True
    )
    # ### end Alembic commands ###
