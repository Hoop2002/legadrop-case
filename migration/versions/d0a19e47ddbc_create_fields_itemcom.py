"""create fields itemcom

Revision ID: d0a19e47ddbc
Revises: 9f02754b56b6
Create Date: 2023-12-03 10:01:44.933466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d0a19e47ddbc"
down_revision: Union[str, None] = "9f02754b56b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
