# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    priority = fields.Selection(
        [("0", "Low"), ("1", "Normal"), ("2", "High"), ("3", "Very High")],
        default="0",
        help="Helps prioritize BoM.",
    )

    def search(self, args, **kwargs):
        if self.env.context.get("mrp_bom_priority_change_order"):
            kwargs["order"] = "priority DESC, sequence, product_id, id"
        return super().search(args, **kwargs)

    @api.model
    def _bom_find(self, args, **kwargs):
        return super(
            MrpBom, self.with_context(mrp_bom_priority_change_order=True)
        )._bom_find(args, **kwargs)
