"""archdioceses added

Revision ID: dff218d6cbe7
Revises: b8938ff60c26
Create Date: 2020-05-14 14:18:03.477945

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dff218d6cbe7'
down_revision = 'b8938ff60c26'
branch_labels = ()
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('archdioceses',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('status', sa.SmallInteger(), server_default='1', nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('districts', sa.Column('address', sa.String(length=255), nullable=True))
    op.add_column('districts', sa.Column('archdiocese_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'districts', 'archdioceses', ['archdiocese_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'districts', type_='foreignkey')
    op.drop_column('districts', 'archdiocese_id')
    op.drop_column('districts', 'address')
    op.drop_table('archdioceses')
    # ### end Alembic commands ###
