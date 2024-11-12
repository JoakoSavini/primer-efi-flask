"""primero user

Revision ID: fd70a9f88c4a
Revises: 
Create Date: 2024-11-05 20:11:16.517440

"""
from alembic import op
import sqlalchemy as sa

from werkzeug.security import generate_password_hash
from models import User
from app import db


# revision identifiers, used by Alembic.
revision = 'fd70a9f88c4a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password_hash', sa.String(length=300), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
    
    existing_user = User.query.filter_by(username='admin').first()
    
    if not existing_user:
        admin_user = User(
            username='admin',
            password_hash=generate_password_hash('admin'),
            is_admin=True,
        )
        db.session.add(admin_user)
        db.session.commit()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###