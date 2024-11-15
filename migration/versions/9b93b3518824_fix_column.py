"""fix column

Revision ID: 9b93b3518824
Revises: 967a42b45e65
Create Date: 2024-01-22 14:29:40.108396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9b93b3518824"
down_revision: Union[str, None] = "967a42b45e65"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users_items", "count")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users_items",
        sa.Column("count", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    # ### end Alembic commands ###
