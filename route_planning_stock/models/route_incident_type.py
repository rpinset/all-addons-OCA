# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.exceptions import UserError


class RouteIncidentType(models.Model):
    _inherit = "route.incident.type"

    @api.ondelete(at_uninstall=False)
    def _unlink_except_picking_cancel(self):
        for record in self:
            metadatas = record.get_metadata()
            if (
                metadatas
                and metadatas[0].get("xmlid")
                == "route_planning_stock.route_incident_cancel"
            ):
                raise UserError(
                    self.env._(
                        "You cannot delete this incident type, "
                        "it is necessary for pickings cancellation."
                    )
                )
