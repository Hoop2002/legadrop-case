"""add moogolg

Revision ID: b078c9e455ae
Revises: 828f7b60072b
Create Date: 2023-12-03 10:24:56.337274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b078c9e455ae"
down_revision: Union[str, None] = "828f7b60072b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
