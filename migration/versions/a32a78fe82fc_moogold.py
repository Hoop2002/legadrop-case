"""moogold

Revision ID: a32a78fe82fc
Revises: 9f122d77abd0
Create Date: 2023-12-03 10:29:28.554528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a32a78fe82fc"
down_revision: Union[str, None] = "9f122d77abd0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("item_compounds", sa.Column("moogold_id", sa.String(), nullable=True))
    op.add_column("item_compounds", sa.Column("test", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("item_compounds", "test")
    op.drop_column("item_compounds", "moogold_id")
    # ### end Alembic commands ###
