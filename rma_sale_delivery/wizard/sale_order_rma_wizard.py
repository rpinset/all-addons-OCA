# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderRmaWizard(models.TransientModel):
    _inherit = "sale.order.rma.wizard"

    company_id = fields.Many2one(
        comodel_name="res.company", default=lambda self: self.env.company
    )
    rma_reception_strategy = fields.Selection(
        related="company_id.rma_reception_strategy"
    )
    reception_carrier_id = fields.Many2one(
        comodel_name="delivery.carrier", string="Reception Carrier"
    )


class SaleOrderLineRmaWizard(models.TransientModel):
    _inherit = "sale.order.line.rma.wizard"

    def _prepare_rma_values(self):
        values = super()._prepare_rma_values()
        if self.wizard_id.reception_carrier_id:
            values["reception_carrier_id"] = self.wizard_id.reception_carrier_id.id
        return values
