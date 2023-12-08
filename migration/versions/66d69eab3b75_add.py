"""add

Revision ID: 66d69eab3b75
Revises: d0a19e47ddbc
Create Date: 2023-12-03 10:10:14.454718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "66d69eab3b75"
down_revision: Union[str, None] = "d0a19e47ddbc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
