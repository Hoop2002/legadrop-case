"""empty message

Revision ID: e05de2d4cae4
Revises: 775cb5e1d219
Create Date: 2023-11-05 22:43:14.416229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e05de2d4cae4'
down_revision: Union[str, None] = '775cb5e1d219'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('test', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test', 'test')
    # ### end Alembic commands ###
