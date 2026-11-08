# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MercadoLibrePartner(models.Model):
    _name = "mercadolibre.res.partner"
    _inherit = "mercadolibre.binding"
    _description = "Mercado Libre Buyer"

    odoo_id = fields.Many2one(
        comodel_name="res.partner",
        required=True,
        ondelete="cascade",
        index=True,
    )
    backend_id = fields.Many2one(
        comodel_name="mercadolibre.backend",
        required=True,
        ondelete="restrict",
        index=True,
    )
    external_id = fields.Char(required=True, index=True)
    nickname = fields.Char()
    billing_doc_type = fields.Char(string="Billing Document Type")
    billing_doc_number = fields.Char(string="Billing Document Number")
    raw_billing = fields.Json(
        groups="connector_mercadolibre.group_mercadolibre_manager",
    )

    _partner_external_unique = models.Constraint(
        "UNIQUE(backend_id, external_id)",
        "This Mercado Libre buyer is already imported.",
    )
