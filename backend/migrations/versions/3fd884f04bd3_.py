"""empty message

Revision ID: 3fd884f04bd3
Revises: e65f317a2c9a
Create Date: 2024-03-18 13:25:57.288299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fd884f04bd3'
down_revision = 'e65f317a2c9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Customer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subject', sa.String(), nullable=True))
        batch_op.create_unique_constraint(None, ['subject'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Customer', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('subject')

    # ### end Alembic commands ###
