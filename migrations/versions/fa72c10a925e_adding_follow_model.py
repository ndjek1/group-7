"""Adding Follow model 

Revision ID: fa72c10a925e
Revises: 9d329e93b0d9
Create Date: 2024-07-25 11:52:17.809699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa72c10a925e'
down_revision = '9d329e93b0d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follow',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followee_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['followee_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('follower_id', 'followee_id', name='unique_follow')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('follow')
    # ### end Alembic commands ###
