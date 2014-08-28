"""empty message

Revision ID: 4df69c261a5e
Revises: 145a2977086a
Create Date: 2014-08-08 01:55:22.269000

"""

# revision identifiers, used by Alembic.
revision = '4df69c261a5e'
down_revision = '145a2977086a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('like', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'like')
    ### end Alembic commands ###