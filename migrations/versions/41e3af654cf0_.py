"""empty message

Revision ID: 41e3af654cf0
Revises: 
Create Date: 2020-02-17 22:01:59.615399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41e3af654cf0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('club_session',
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('max_bakers', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('session_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('is_guest', sa.Boolean(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('baked_offset', sa.Integer(), nullable=True),
    sa.Column('eaten_offset', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('baker_membership',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['club_session.session_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], )
    )
    op.create_table('clubsession_membership',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['club_session.session_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clubsession_membership')
    op.drop_table('baker_membership')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('club_session')
    # ### end Alembic commands ###
