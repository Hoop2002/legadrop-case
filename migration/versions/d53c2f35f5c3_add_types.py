"""add types

Revision ID: d53c2f35f5c3
Revises: 8cf2d7da46ea
Create Date: 2024-01-26 15:21:27.812873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "d53c2f35f5c3"
down_revision: Union[str, None] = "8cf2d7da46ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conditions_types = postgresql.ENUM("calcs", "time", name="condition_types")
    conditions_types.create(op.get_bind())
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "conditions",
        sa.Column(
            "type_condition",
            postgresql.ENUM("calcs", "time", name="condition_types"),
            server_default="calcs",
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("conditions", "type_condition")
    # ### end Alembic commands ###
    conditions_types = postgresql.ENUM("calcs", "time", name="condition_types")
    conditions_types.drop(op.get_bind())
