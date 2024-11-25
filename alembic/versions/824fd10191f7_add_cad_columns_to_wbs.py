"""add_cad_columns_to_wbs

Revision ID: <auto_generated>
Revises: 950d1784f10c
Create Date: <auto_generated>

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '<auto_generated>'
down_revision = '950d1784f10c'  # Make sure this points to your last successful migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns
    op.add_column('wbs', sa.Column('cadAdmins', sa.String(), nullable=True))
    op.add_column('wbs', sa.Column('cadCoords', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove columns
    op.drop_column('wbs', 'cadAdmins')
    op.drop_column('wbs', 'cadCoords')