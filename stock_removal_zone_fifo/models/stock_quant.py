# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    # Existing rows are filled by pre_init_hook, new ones by create().
    zone_in_date = fields.Datetime(
        string="Zone Entry Date",
        required=True,
        default=fields.Datetime.now,
        index=True,
        readonly=True,
        help="Date at which these goods entered the storage zone they are"
        " stored in.\n"
        "It differs from the incoming date on two points: it is not reset when"
        " stock is merged into the quant, and it is kept when the goods are"
        " moved between two locations of the same zone.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Goods enter their zone when they are put in a location. Always
            # set, so the removal sort stays a plain ASC sort.
            if not vals.get("zone_in_date"):
                vals["zone_in_date"] = vals.get("in_date") or fields.Datetime.now()
        return super().create(vals_list)

    @api.model
    def _get_inventory_fields_create(self):
        return super()._get_inventory_fields_create() + ["zone_in_date"]

    @api.model
    def _get_removal_strategy_order(self, removal_strategy):
        if removal_strategy == "zone_fifo":
            return "zone_in_date, in_date, id"
        return super()._get_removal_strategy_order(removal_strategy)
