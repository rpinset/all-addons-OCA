# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    # The reservation moves created on the blanket order when a call-off order
    # was processed were wrongly linked to the call-off order line.
    cr.execute(
        """
        UPDATE stock_move
        SET call_off_sale_line_id = NULL
        WHERE used_for_sale_reservation IS TRUE
        AND call_off_sale_line_id IS NOT NULL
        """
    )
    _logger.info("%s reservation moves unlinked from call-off order lines", cr.rowcount)
