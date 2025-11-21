# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def write(self, vals):
        if "owner_id" in vals:
            for production in self:
                if production.owner_restriction != "standard_behavior":
                    production.move_line_raw_ids.unlink()
        return super().write(vals)
