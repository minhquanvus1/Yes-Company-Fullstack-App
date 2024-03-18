"""empty message

Revision ID: e65f317a2c9a
Revises: 
Create Date: 2024-03-17 13:20:15.742990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e65f317a2c9a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('OrderItem', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_order_product', ['order_id', 'product_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('OrderItem', schema=None) as batch_op:
        batch_op.drop_constraint('unique_order_product', type_='unique')

    # ### end Alembic commands ###