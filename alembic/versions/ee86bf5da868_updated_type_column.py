"""updated type column

Revision ID: ee86bf5da868
Revises: 2ad31cbe9860
Create Date: 2025-06-24 01:01:00.409631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ee86bf5da868'
down_revision: Union[str, Sequence[str], None] = '2ad31cbe9860'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop default value first
    op.execute("ALTER TABLE transactions ALTER COLUMN transaction_type DROP DEFAULT;")

    # Change ENUM to INTEGER
    op.execute("""
        ALTER TABLE transactions
        ALTER COLUMN transaction_type TYPE INTEGER
        USING (
            CASE transaction_type
                WHEN 'income' THEN 0
                WHEN 'expense' THEN 1
            END
        );
    """)

    # Set new integer default
    op.execute("ALTER TABLE transactions ALTER COLUMN transaction_type SET DEFAULT 1;")

    # Drop the enum type
    op.execute("DROP TYPE IF EXISTS transaction_type_enum;")


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate the enum type
    op.execute("CREATE TYPE transaction_type_enum AS ENUM ('income', 'expense', 'transfer');")

    # Drop the current integer default before converting the column
    op.execute("ALTER TABLE transactions ALTER COLUMN transaction_type DROP DEFAULT;")

    # Convert integer values back to enum text and change type
    op.execute("""
        ALTER TABLE transactions
        ALTER COLUMN transaction_type TYPE transaction_type_enum
        USING (
            CASE transaction_type
                WHEN 0 THEN 'income'
                WHEN 1 THEN 'expense'
            END
        );
    """)

    # Set default to 'expense'
    op.execute("ALTER TABLE transactions ALTER COLUMN transaction_type SET DEFAULT 'expense';")
