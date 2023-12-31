"""empty message

Revision ID: 1d841888e18e
Revises: 16d4472f7b65
Create Date: 2023-11-06 20:21:11.255833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d841888e18e'
down_revision: Union[str, None] = '16d4472f7b65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'telegram_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'telegram_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
