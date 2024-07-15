"""Add profile fields to User model

Revision ID: 359db50163ab
Revises: 3e0270dc4170
Create Date: 2024-07-14 12:36:54.104167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '359db50163ab'
down_revision = '3e0270dc4170'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=30), nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.String(length=30), nullable=True))
        batch_op.add_column(sa.Column('phone', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('address', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('education', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('country', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('state', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('experience', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('additional_details', sa.String(length=200), nullable=True))

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('first_name')
        batch_op.drop_column('last_name')
        batch_op.drop_column('phone')
        batch_op.drop_column('address')
        batch_op.drop_column('education')
        batch_op.drop_column('country')
        batch_op.drop_column('state')
        batch_op.drop_column('experience')
        batch_op.drop_column('additional_details')


    # ### end Alembic commands ###
