"""store credit as float

Revision ID: b7c2e4a91d08
Revises: f3a91c2e7b04
Create Date: 2026-10-14 23:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b7c2e4a91d08"
down_revision: Union[str, Sequence[str], None] = "f3a91c2e7b04"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "credit",
        existing_type=sa.Integer(),
        type_=sa.Float(),
        postgresql_using="credit::double precision",
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "credit",
        existing_type=sa.Float(),
        type_=sa.Integer(),
        postgresql_using="credit::integer",
    )
