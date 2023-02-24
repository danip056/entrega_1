"""First commit

Revision ID: 8e74eee70e3f
Revises: 
Create Date: 2023-02-21 17:09:51.307408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e74eee70e3f'
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