# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

_logger = logging.getLogger(__name__)


def pre_init_hook(env):
    # Create the column already filled, so the ORM finds nothing to backfill.
    # The incoming date is the best guess of when the goods entered their zone.
    env.cr.execute(
        """
        ALTER TABLE stock_quant ADD COLUMN IF NOT EXISTS zone_in_date timestamp;
        UPDATE stock_quant SET zone_in_date = in_date WHERE zone_in_date IS NULL;
        """
    )
    _logger.info("Initialized zone_in_date on %s quants", env.cr.rowcount)
