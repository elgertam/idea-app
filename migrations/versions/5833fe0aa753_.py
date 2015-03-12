"""Add members table. Modifies idea and user tables.

Revision ID: 5833fe0aa753
Revises: 3c3c699f0270
Create Date: 2015-05-17 00:10:06.865511

"""

# revision identifiers, used by Alembic.
revision = '5833fe0aa753'
down_revision = '3c3c699f0270'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('members',
                    sa.Column('idea', sa.Integer(), nullable=True),
                    sa.Column('user', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['idea'], ['idea.id'], name=op.f('fk_members_idea_idea')),
                    sa.ForeignKeyConstraint(['user'], ['user.id'], name=op.f('fk_members_user_user'))
                    )
    op.add_column('idea', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_idea_owner_id_user'), 'idea', 'user', ['owner_id'], ['id'])


def downgrade():
    op.drop_constraint(op.f('fk_idea_owner_id_user'), 'idea', type_='foreignkey')
    op.drop_column('idea', 'owner_id')

    op.drop_table('members')
