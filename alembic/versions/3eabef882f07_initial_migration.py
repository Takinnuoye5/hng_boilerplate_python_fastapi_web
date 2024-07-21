"""Initial migration

Revision ID: 3eabef882f07
Revises: 534047ee3520
Create Date: 2024-07-21 22:07:44.921404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3eabef882f07'
down_revision: Union[str, None] = '534047ee3520'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('newsletters')
    op.add_column('permissions', sa.Column('description', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('permissions', 'description')
    op.create_table('newsletters',
    sa.Column('id', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='newsletters_pkey'),
    sa.UniqueConstraint('email', name='newsletters_email_key')
    )
    # ### end Alembic commands ###
