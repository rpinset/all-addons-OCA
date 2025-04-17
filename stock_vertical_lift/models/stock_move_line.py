# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    vertical_lift_skipped = fields.Boolean(
        "Skipped in Vertical Lift?",
        help="If this flag is set, it means that when the move "
        "was being processed in the Vertical Lift, the operator decided to "
        "skip its processing.",
    )

    def fetch_vertical_lift_tray_source(self):
        self.ensure_one()
        self.location_id.fetch_vertical_lift_tray()
        return {"type": "ir.actions.client", "tag": "soft_reload"}

    def fetch_vertical_lift_tray_dest(self):
        self.ensure_one()
        self.location_dest_id.fetch_vertical_lift_tray()
        return {"type": "ir.actions.client", "tag": "soft_reload"}
