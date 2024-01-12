"""itemf_create_at

Revision ID: 55c292560c9a
Revises: 760b58596bcb
Create Date: 2023-12-20 11:22:24.367161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55c292560c9a'
down_revision: Union[str, None] = '760b58596bcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items_findings', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items_findings', 'created_at')
    # ### end Alembic commands ###
