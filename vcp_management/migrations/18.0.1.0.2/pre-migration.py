# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return

    _logger.info(
        "Safely casting 'color' from VARCHAR to INTEGER in vcp_request_label..."
    )

    # 1. First, handle any edge cases where color might be empty or not a number
    cr.execute("""
        UPDATE vcp_request_label
        SET color = '0'
        WHERE color IS NULL OR color = '' OR color !~ '^[0-9]+$';
    """)

    # 2. Use the 'USING' clause to safely cast the strings to integers
    cr.execute("""
        ALTER TABLE vcp_request_label
        ALTER COLUMN color TYPE int4 USING color::integer;
    """)

    _logger.info("Successfully converted 'color' column.")
