"""First db version

Revision ID: 1bbfa080d9a3
Revises: 
Create Date: 2023-02-23 23:31:24.293849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bbfa080d9a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('user')
    )
    op.create_table('task',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('original_file_name', sa.String(length=300), nullable=True),
    sa.Column('original_file_ext', sa.String(length=10), nullable=True),
    sa.Column('original_stored_file_name', sa.String(length=300), nullable=True),
    sa.Column('target_file_ext', sa.String(length=10), nullable=True),
    sa.Column('target_stored_file_name', sa.String(length=300), nullable=True),
    sa.Column('uploaded_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('status', sa.Enum('uploaded', 'processed', name='status_types'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    op.drop_table('user')
    # ### end Alembic commands ###