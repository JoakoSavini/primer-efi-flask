"""empty message

Revision ID: cab46770b037
Revises: 6223b8122739
Create Date: 2024-07-19 13:52:23.612029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cab46770b037'
down_revision = '6223b8122739'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('celular', schema=None) as batch_op:
        batch_op.add_column(sa.Column('usado', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('stock', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('categoria_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'categoria', ['categoria_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('celular', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('categoria_id')
        batch_op.drop_column('stock')
        batch_op.drop_column('usado')

    # ### end Alembic commands ###