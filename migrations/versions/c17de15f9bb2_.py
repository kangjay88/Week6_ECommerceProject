"""empty message

Revision ID: c17de15f9bb2
Revises: c0865c8f5f81
Create Date: 2022-09-13 10:13:31.033908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c17de15f9bb2'
down_revision = 'c0865c8f5f81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=150), nullable=False),
    sa.Column('img_url', sa.String(length=300), nullable=True),
    sa.Column('description', sa.String(length=300), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cart',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cart')
    op.drop_table('product')
    # ### end Alembic commands ###
