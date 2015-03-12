"""Rename columns. Set nullability.

Revision ID: 51b72851fbfc
Revises: 5833fe0aa753
Create Date: 2015-05-17 01:48:26.139561

"""

# revision identifiers, used by Alembic.
revision = '51b72851fbfc'
down_revision = '5833fe0aa753'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('idea', 'problem_description', new_column_name='problem', nullable=False)
    op.alter_column('idea', 'solution_description', new_column_name='solution', nullable=False)
    op.alter_column('user', 'active', existing_type=sa.Boolean(), nullable=False)
    op.alter_column('user', 'password', existing_type=sa.String(length=100), nullable=False)


def downgrade():
    op.alter_column('user', 'password', existing_type=sa.String(length=100), nullable=True)
    op.alter_column('user', 'active', existing_type=sa.Boolean(), nullable=True)
    op.alter_column('idea', 'problem', new_column_name='problem_description', nullable=True)
    op.alter_column('idea', 'solution', new_column_name='solution_description', nullable=True)
