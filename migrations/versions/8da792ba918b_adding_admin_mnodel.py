"""Adding Admin mnodel 

Revision ID: 8da792ba918b
Revises: 77f3572d88da
Create Date: 2024-07-24 17:18:09.148560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8da792ba918b'
down_revision = '77f3572d88da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('link', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('category', sa.String(length=25), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('category')
        batch_op.drop_column('link')

    op.drop_table('admin')
    # ### end Alembic commands ###