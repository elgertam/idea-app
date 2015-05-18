"""Added archive field on idea. Set primary key on members table.

Revision ID: eb853ed52c6
Revises: 51b72851fbfc
Create Date: 2015-05-17 15:04:36.004793

"""

# revision identifiers, used by Alembic.
revision = 'eb853ed52c6'
down_revision = '51b72851fbfc'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('idea', sa.Column('archive', sa.Boolean(), nullable=False, server_default='FALSE'))
    op.alter_column('members', 'idea', existing_type=sa.Integer(), nullable=False)
    op.alter_column('members', 'user', existing_type=sa.Integer(), nullable=False)
    op.create_primary_key('pk_members', 'members', ['idea', 'user'])


def downgrade():
    op.drop_column('idea', 'archive')
    op.alter_column('members', 'idea', existing_type=sa.Integer(), nullable=True)
    op.alter_column('members', 'user', existing_type=sa.Integer(), nullable=True)
    op.drop_constraint('pk_members', 'members', type_='primary')
