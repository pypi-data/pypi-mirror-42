"""Adding base attributes to issues

Revision ID: 8a9532dbe303
Revises: 397dcb772234
Create Date: 2019-01-15 13:49:47.122308

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = '8a9532dbe303'
down_revision = '397dcb772234'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('issues', sa.Column('created', mysql.DATETIME(), server_default=sa.text('now()'), nullable=False))
    op.add_column('issues', sa.Column('updated', mysql.DATETIME(), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('issues', 'updated')
    op.drop_column('issues', 'created')
    # ### end Alembic commands ###
