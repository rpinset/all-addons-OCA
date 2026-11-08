# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MercadoLibreWarehouseMapping(models.Model):
    _name = "mercadolibre.warehouse.mapping"
    _description = "Mercado Libre Warehouse Mapping"
    _order = "id"

    backend_id = fields.Many2one(
        comodel_name="mercadolibre.backend",
        required=True,
        ondelete="cascade",
        index=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        related="backend_id.company_id",
        store=True,
    )
    warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse",
        required=True,
        domain="[('company_id', '=', company_id)]",
    )
    store_id = fields.Char(string="Store ID")
    network_node_id = fields.Char()
    stock_type = fields.Selection(
        selection=[
            ("seller_warehouse", "Seller warehouse"),
            ("selling_address", "Selling address"),
            ("fulfillment", "Fulfillment"),
        ],
        required=True,
        default="seller_warehouse",
    )
    location_id = fields.Many2one(
        comodel_name="stock.location",
        related="warehouse_id.lot_stock_id",
        store=True,
    )

    _warehouse_stock_type_unique = models.Constraint(
        "UNIQUE(backend_id, warehouse_id, stock_type)",
        "This warehouse is already mapped for that stock type.",
    )
