"""merge heads

Revision ID: c1e03dcf8e53
Revises: b24f03d72bf9, bd35f5761bab
Create Date: 2024-07-20 07:25:39.703627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1e03dcf8e53'
down_revision = ('b24f03d72bf9', 'bd35f5761bab')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
