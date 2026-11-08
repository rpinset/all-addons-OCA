# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    mercadolibre_shipment_id = fields.Many2one(
        comodel_name="mercadolibre.shipment",
        string="Mercado Libre Shipment",
        copy=False,
        index=True,
    )
    mercadolibre_logistic_type = fields.Char(
        related="mercadolibre_shipment_id.logistic_type",
        string="Logistic Type",
    )
    mercadolibre_tracking_number = fields.Char(
        related="mercadolibre_shipment_id.tracking_number",
        string="Mercado Libre Tracking",
    )
