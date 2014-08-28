"""empty message

Revision ID: 1bc3a37f02cc
Revises: None
Create Date: 2014-08-29 00:18:27.687000

"""

# revision identifiers, used by Alembic.
revision = '1bc3a37f02cc'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location_first',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location_first', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location_second',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location_second', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('teamname', sa.String(length=255), nullable=True),
    sa.Column('location_first', sa.String(length=255), nullable=True),
    sa.Column('location_second', sa.String(length=255), nullable=True),
    sa.Column('university', sa.String(length=255), nullable=True),
    sa.Column('Introduce', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team')
    op.drop_table('location_second')
    op.drop_table('location_first')
    ### end Alembic commands ###
