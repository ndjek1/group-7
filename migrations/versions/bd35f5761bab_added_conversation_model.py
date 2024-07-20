"""Added conversation model

Revision ID: bd35f5761bab
Revises: 9dcb55a2c2cf
Create Date: 2024-07-19 12:41:06.445842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd35f5761bab'
down_revision = '9dcb55a2c2cf'
branch_labels = None
depends_on = None


def upgrade():
    # Check if the table already exists
    conn = op.get_bind()
    if not conn.dialect.has_table(conn, 'conversation'):
        op.create_table('conversation',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user1_id', sa.Integer(), nullable=False),
            sa.Column('user2_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['user1_id'], ['user.id'], name='fk_conversation_user1_id'),
            sa.ForeignKeyConstraint(['user2_id'], ['user.id'], name='fk_conversation_user2_id'),
            sa.PrimaryKeyConstraint('id')
        )

    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('date_sent', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('conversation_id', sa.Integer(), nullable=False))

        # Create foreign key constraints with names
        batch_op.create_foreign_key(
            'fk_message_sender_id_user',  # Constraint name
            'user', ['sender_id'], ['id']
        )
        batch_op.create_foreign_key(
            'fk_message_conversation_id_conversation',  # Constraint name
            'conversation', ['conversation_id'], ['id']
        )

        # Drop old columns
        batch_op.drop_column('timestamp')
        batch_op.drop_column('receiver_id')
        batch_op.drop_column('message')


def downgrade():
    # Revert the message table changes
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('message', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('receiver_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=True))

        # Drop foreign key constraints with names
        batch_op.drop_constraint('fk_message_conversation_id_conversation', type_='foreignkey')
        batch_op.drop_constraint('fk_message_sender_id_user', type_='foreignkey')

        # Drop new columns
        batch_op.drop_column('conversation_id')
        batch_op.drop_column('date_sent')
        batch_op.drop_column('content')

    # Drop the conversation table
    if op.get_bind().dialect.has_table(op.get_bind(), 'conversation'):
        op.drop_table('conversation')
