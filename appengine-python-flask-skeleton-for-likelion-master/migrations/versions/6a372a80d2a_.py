"""empty message

Revision ID: 6a372a80d2a
Revises: 519c59820842
Create Date: 2014-09-14 23:26:05.578000

"""

# revision identifiers, used by Alembic.
revision = '6a372a80d2a'
down_revision = '519c59820842'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('teamname', sa.String(length=255), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('university', sa.String(length=255), nullable=True),
    sa.Column('Introduce', sa.Text(), nullable=True),
    sa.Column('favorite_date', sa.String(length=255), nullable=True),
    sa.Column('favorite_place', sa.String(length=255), nullable=True),
    sa.Column('ranking_score', sa.Integer(), nullable=True),
    sa.Column('ranking_result', sa.String(length=255), nullable=True),
    sa.Column('leader_name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team')
    ### end Alembic commands ###