"""add 123

Revision ID: 828f7b60072b
Revises: 66d69eab3b75
Create Date: 2023-12-03 10:11:37.168617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "828f7b60072b"
down_revision: Union[str, None] = "66d69eab3b75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
