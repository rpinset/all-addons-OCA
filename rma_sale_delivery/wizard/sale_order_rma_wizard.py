# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderRmaWizard(models.TransientModel):
    _inherit = "sale.order.rma.wizard"

    company_id = fields.Many2one(
        comodel_name="res.company", default=lambda self: self.env.company
    )
    rma_reception_strategy = fields.Selection(
        related="company_id.rma_reception_strategy"
    )
    available_reception_carrier_ids = fields.Many2many(
        comodel_name="delivery.carrier",
        compute="_compute_available_reception_carrier_ids",
    )
    reception_carrier_id = fields.Many2one(
        comodel_name="delivery.carrier",
        string="Reception Carrier",
        domain="[('id', 'in', available_reception_carrier_ids)]",
    )

    @api.depends("partner_shipping_id", "order_id.partner_shipping_id")
    def _compute_available_reception_carrier_ids(self):
        carrier_model = self.env["delivery.carrier"]
        for item in self:
            partner = item.partner_shipping_id or item.order_id.partner_shipping_id
            carriers = carrier_model.search(
                carrier_model._check_company_domain(item.company_id)
            )
            item.available_reception_carrier_ids = (
                carriers.available_carriers_rma(partner, item.order_id)
                if partner
                else carriers
            )


class SaleOrderLineRmaWizard(models.TransientModel):
    _inherit = "sale.order.line.rma.wizard"

    def _prepare_rma_values(self):
        values = super()._prepare_rma_values()
        if self.wizard_id.reception_carrier_id:
            values["reception_carrier_id"] = self.wizard_id.reception_carrier_id.id
        return values
