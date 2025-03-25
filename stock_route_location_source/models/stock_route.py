# Copyright 2023 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models


class StockRoute(models.Model):
    _inherit = "stock.route"

    def _get_source_location(self, dest_location):
        self.ensure_one()
        dest_location.ensure_one()
        src_location = self.env["stock.location"]
        while True:
            values = {}
            _dest_location = src_location or dest_location
            if not src_location:
                values["route_ids"] = self
            rule = self.env["procurement.group"]._get_rule(
                self.env["product.product"], _dest_location, values
            )
            if not rule or rule.action not in ["pull", "pull_push"]:
                break
            src_location = rule.location_src_id
            if rule.procure_method == "make_to_stock":
                break
        return src_location
