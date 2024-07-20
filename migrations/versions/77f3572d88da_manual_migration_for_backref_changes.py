"""Manual migration for backref changes

Revision ID: 77f3572d88da
Revises: 1fe14a477d10
Create Date: 2024-07-20 08:01:18.921907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77f3572d88da'
down_revision = '1fe14a477d10'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
