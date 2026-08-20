# Copyright 2026 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Move the RKSV receipt number from ``sequence_number`` to ``asign_seq``.

    Each RKSV POS gets a dedicated gapless sequence (``asign_seq_id``) whose
    next value continues right after the highest already signed receipt number.
    Existing orders keep their ``asign_seq`` (it is part of the signature), so
    nothing is renumbered.
    """
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})
    sequence_model = env["ir.sequence"].sudo()
    configs = env["pos.config"].search([("asign_enabled", "=", True)])

    for config in configs:
        if config.asign_seq_id:
            continue

        cr.execute(
            """
            SELECT COALESCE(MAX(asign_seq), 0)
              FROM pos_order
             WHERE config_id = %s
               AND asign_state = 's'
            """,
            (config.id,),
        )
        max_seq = cr.fetchone()[0] or 0

        config.asign_seq_id = sequence_model.create(
            {
                "name": f"RKSV {config.asign_pid or config.name}",
                "implementation": "no_gap",
                "padding": 0,
                "number_increment": 1,
                "number_next": max_seq + 1,
                "company_id": config.company_id.id,
            }
        )
        _logger.info(
            "RKSV: created receipt sequence for POS %s starting at %s",
            config.name,
            max_seq + 1,
        )
