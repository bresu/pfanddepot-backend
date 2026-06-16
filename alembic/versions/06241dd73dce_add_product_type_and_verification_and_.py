"""add product type and verification and supermarket enums

Revision ID: 06241dd73dce
Revises: 4be40e86b517
Create Date: 2026-06-16 15:20:22.178495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06241dd73dce'
down_revision: Union[str, Sequence[str], None] = '4be40e86b517'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column("product_type", sa.String(), nullable=False, server_default="bottle"),
    )
    op.add_column(
        "products",
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_column("products", "is_verified")
    op.drop_column("products", "product_type")
