# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RmaRmaWizard(models.TransientModel):
    _inherit = "rma.rma.wizard"

    domain_operation_id = fields.Binary(compute="_compute_domain_operation_id")
    operation_id = fields.Many2one(domain="domain_operation_id")
    reason_id = fields.Many2one(
        comodel_name="rma.reason",
        string="Reason",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        rma_id = self.env.context.get("active_id")
        rma = self.env["rma"].browse(rma_id)
        if rma:
            res.update(
                reason_id=rma.reason_id.id,
            )
        return res

    @api.onchange("reason_id")
    def _onchange_reason_id(self):
        """Avoid incompatibilities."""
        allowed_operations = self.reason_id.allowed_operation_ids
        if self.reason_id and allowed_operations and self.operation_id:
            if self.operation_id not in allowed_operations:
                if len(allowed_operations) == 1:
                    self.operation_id = fields.first(allowed_operations)
                else:
                    self.operation_id = False

    @api.depends("reason_id")
    def _compute_domain_operation_id(self):
        for item in self:
            domain = []
            if item.reason_id.allowed_operation_ids:
                domain = [("id", "in", item.reason_id.allowed_operation_ids.ids)]
            item.domain_operation_id = domain

    def _stock_return_picking_vals(self, picking):
        vals = super()._stock_return_picking_vals(picking)
        if self.reason_id:
            vals["rma_reason_id"] = self.reason_id.id
        return vals
