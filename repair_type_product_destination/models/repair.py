# Copyright 2024 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    product_location_dest_id = fields.Many2one(
        "stock.location",
        "Product Destination Location",
        compute="_compute_product_location_dest_id",
        store=True,
        required=True,
        precompute=True,
        index=True,
        check_company=True,
        help="This is the location where the repaired product will be stored.",
    )

    @api.depends("picking_type_id")
    def _compute_product_location_dest_id(self):
        for repair in self:
            repair.product_location_dest_id = (
                repair.picking_type_id.default_product_location_dest_id
            )
