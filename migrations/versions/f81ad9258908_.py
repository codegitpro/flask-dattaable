"""empty message

Revision ID: f81ad9258908
Revises: 
Create Date: 2020-08-03 04:31:17.413496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f81ad9258908'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Contract',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('contract_title', sa.String(), nullable=True),
    sa.Column('discord', sa.String(), nullable=True),
    sa.Column('refund', sa.String(), nullable=True),
    sa.Column('trader', sa.String(), nullable=True),
    sa.Column('payment_options', sa.String(), nullable=True),
    sa.Column('payment_amount', sa.Float(), nullable=True),
    sa.Column('contract_details', sa.String(), nullable=True),
    sa.Column('contracter', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Contract_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contract_title', sa.String(), nullable=True),
    sa.Column('contracter', sa.String(), nullable=True),
    sa.Column('contractee', sa.String(), nullable=True),
    sa.Column('update', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Contracts_final',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contractee', sa.String(), nullable=True),
    sa.Column('contract_title', sa.String(), nullable=True),
    sa.Column('discord', sa.String(), nullable=True),
    sa.Column('refund', sa.String(), nullable=True),
    sa.Column('trader', sa.String(), nullable=True),
    sa.Column('payment_options', sa.String(), nullable=True),
    sa.Column('payment_amount', sa.Float(), nullable=True),
    sa.Column('contract_details', sa.String(), nullable=True),
    sa.Column('contracter', sa.String(), nullable=True),
    sa.Column('pending', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.Binary(), nullable=True),
    sa.Column('funds', sa.Float(), nullable=True),
    sa.Column('reputation', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('C_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('c_id', sa.Integer(), nullable=False),
    sa.Column('update', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('user_one', sa.Integer(), nullable=True),
    sa.Column('user_two', sa.Integer(), nullable=True),
    sa.Column('complete', sa.Integer(), nullable=True),
    sa.Column('cancel', sa.Integer(), nullable=True),
    sa.Column('dispute', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['c_id'], ['Contracts_final.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('C_status')
    op.drop_table('User')
    op.drop_table('Contracts_final')
    op.drop_table('Contract_status')
    op.drop_table('Contract')
    # ### end Alembic commands ###
