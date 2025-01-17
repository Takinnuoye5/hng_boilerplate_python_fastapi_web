"""removed is_superadmin to user table

Revision ID: 70250910fff9
Revises: 164db40f2a51
Create Date: 2024-07-23 11:19:37.383103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70250910fff9'
down_revision: Union[str, None] = '164db40f2a51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_superadmin')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_superadmin', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
