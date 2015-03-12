"""First commit, sets up user and idea tables.

Revision ID: 3c3c699f0270
Revises: None
Create Date: 2015-05-14 22:03:50.559254

"""

# revision identifiers, used by Alembic.
revision = '3c3c699f0270'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('idea',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created', sa.DateTime(), nullable=True),
                    sa.Column('modified', sa.DateTime(), nullable=True),
                    sa.Column('forked_from_id', sa.Integer(), nullable=True),
                    sa.Column('title', sa.String(length=200), nullable=True),
                    sa.Column('problem_description', sa.String(), nullable=True),
                    sa.Column('solution_description', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['forked_from_id'], ['idea.id'], name=op.f('fk_idea_forked_from_id_idea')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_idea'))
                    )

    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created', sa.DateTime(), nullable=True),
                    sa.Column('modified', sa.DateTime(), nullable=True),
                    sa.Column('name', sa.String(length=200), nullable=True),
                    sa.Column('email', sa.String(length=100), nullable=False),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.Column('confirm', sa.String(length=32), nullable=False),
                    sa.Column('password', sa.String(length=100), nullable=True),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
                    sa.UniqueConstraint('confirm', name=op.f('uq_user_confirm')),
                    sa.UniqueConstraint('email', name=op.f('uq_user_email'))
                    )


def downgrade():
    op.drop_table('user')
    op.drop_table('idea')
