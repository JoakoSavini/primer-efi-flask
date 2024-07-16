"""Cambios y arreglos momentaneos en relaciones

Revision ID: 784495b7bbd7
Revises: f43f3b3e48fc
Create Date: 2024-07-15 22:37:33.574070

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '784495b7bbd7'
down_revision = 'f43f3b3e48fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accesorio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.Column('compatibilidad', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('especificacion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ram', sa.Integer(), nullable=False),
    sa.Column('almacenamiento', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('celular_accesorio',
    sa.Column('celular_id', sa.Integer(), nullable=False),
    sa.Column('accesorio_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['accesorio_id'], ['accesorio.id'], ),
    sa.ForeignKeyConstraint(['celular_id'], ['celular.id'], ),
    sa.PrimaryKeyConstraint('celular_id', 'accesorio_id')
    )
    op.create_table('celular_especificacion',
    sa.Column('celular_id', sa.Integer(), nullable=False),
    sa.Column('especificacion_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['celular_id'], ['celular.id'], ),
    sa.ForeignKeyConstraint(['especificacion_id'], ['especificacion.id'], ),
    sa.PrimaryKeyConstraint('celular_id', 'especificacion_id')
    )
    op.drop_table('accesorios')
    with op.batch_alter_table('celular', schema=None) as batch_op:
        batch_op.drop_constraint('celular_ibfk_4', type_='foreignkey')
        batch_op.drop_column('accesorios_id')

    with op.batch_alter_table('modelo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('marca_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'marca', ['marca_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('modelo', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('marca_id')

    with op.batch_alter_table('celular', schema=None) as batch_op:
        batch_op.add_column(sa.Column('accesorios_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('celular_ibfk_4', 'accesorios', ['accesorios_id'], ['id'])

    op.create_table('accesorios',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('nombre', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('compatibilidad', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('celular_especificacion')
    op.drop_table('celular_accesorio')
    op.drop_table('especificacion')
    op.drop_table('accesorio')
    # ### end Alembic commands ###
