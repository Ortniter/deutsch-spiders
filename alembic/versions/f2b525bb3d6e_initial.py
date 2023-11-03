"""initial

Revision ID: f2b525bb3d6e
Revises: 
Create Date: 2023-11-04 01:11:11.284674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2b525bb3d6e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('scraper', sa.Enum('ausbildung', name='scrapers'), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sessions_id'), 'sessions', ['id'], unique=False)
    op.create_index(op.f('ix_sessions_scraper'), 'sessions', ['scraper'], unique=False)
    op.create_index(op.f('ix_sessions_url'), 'sessions', ['url'], unique=False)
    op.create_table('records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('position', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_records_email'), 'records', ['email'], unique=True)
    op.create_index(op.f('ix_records_id'), 'records', ['id'], unique=False)
    op.create_index(op.f('ix_records_name'), 'records', ['name'], unique=False)
    op.create_index(op.f('ix_records_phone'), 'records', ['phone'], unique=False)
    op.create_index(op.f('ix_records_position'), 'records', ['position'], unique=False)
    op.create_index(op.f('ix_records_url'), 'records', ['url'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_records_url'), table_name='records')
    op.drop_index(op.f('ix_records_position'), table_name='records')
    op.drop_index(op.f('ix_records_phone'), table_name='records')
    op.drop_index(op.f('ix_records_name'), table_name='records')
    op.drop_index(op.f('ix_records_id'), table_name='records')
    op.drop_index(op.f('ix_records_email'), table_name='records')
    op.drop_table('records')
    op.drop_index(op.f('ix_sessions_url'), table_name='sessions')
    op.drop_index(op.f('ix_sessions_scraper'), table_name='sessions')
    op.drop_index(op.f('ix_sessions_id'), table_name='sessions')
    op.drop_table('sessions')
    # ### end Alembic commands ###