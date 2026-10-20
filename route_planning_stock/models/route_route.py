# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class RouteRoute(models.Model):
    _inherit = "route.route"

    def _prepare_domain_checkpoint_with_incident(self):
        # It is important to exclude checkpoints that had an incident but for which
        # picking has already been done or cancel
        domain = super()._prepare_domain_checkpoint_with_incident()
        domain += [
            "|",
            ("picking_id", "=", False),
            ("picking_id.state", "not in", ("done", "cancel")),
        ]
        return domain
