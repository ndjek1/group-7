from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '9dcb55a2c2cf'
down_revision = 'b708b31677c4'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Check if columns exist
    columns_exist = 'sender_id' in [col['name'] for col in inspector.get_columns('message')]
    columns_exist = columns_exist and 'receiver_id' in [col['name'] for col in inspector.get_columns('message')]

    if not columns_exist:
        # Add columns
        with op.batch_alter_table('message', schema=None) as batch_op:
            batch_op.add_column(sa.Column('sender_id', sa.Integer(), nullable=False))
            batch_op.add_column(sa.Column('receiver_id', sa.Integer(), nullable=False))

        # Create foreign key constraints
        with op.batch_alter_table('message', schema=None) as batch_op:
            batch_op.create_foreign_key('fk_message_sender_id', 'user', ['sender_id'], ['id'])
            batch_op.create_foreign_key('fk_message_receiver_id', 'user', ['receiver_id'], ['id'])


def downgrade():
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_constraint('fk_message_sender_id', type_='foreignkey')
        batch_op.drop_constraint('fk_message_receiver_id', type_='foreignkey')
        batch_op.drop_column('sender_id')
        batch_op.drop_column('receiver_id')
