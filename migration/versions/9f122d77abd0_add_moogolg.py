"""add moogolg

Revision ID: 9f122d77abd0
Revises: b078c9e455ae
Create Date: 2023-12-03 10:26:29.547898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9f122d77abd0"
down_revision: Union[str, None] = "b078c9e455ae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
