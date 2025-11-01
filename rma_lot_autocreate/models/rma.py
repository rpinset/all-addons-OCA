# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class Rma(models.Model):

    _inherit = "rma"

    def action_confirm(self):
        for rma in self:
            rma._auto_create_lot_if_needed()
        return super().action_confirm()

    def _prepare_rma_lot_vals(self):
        self.ensure_one()
        vals = {
            "name": self.operation_id.lot_sequence_id.next_by_id(),
            "product_id": self.product_id.id,
            "company_id": self.company_id.id,
        }
        if (
            self.product_id.use_expiration_date
            and self.operation_id.lot_expiration_days
        ):
            expiration_date = fields.Date.context_today(self) + relativedelta(
                days=self.operation_id.lot_expiration_days
            )
            removal_date = expiration_date - relativedelta(
                days=self.operation_id.lot_removal_days_before_expiration
            )
            vals["expiration_date"] = expiration_date
            vals["removal_date"] = removal_date
        return vals

    def _auto_create_lot_if_needed(self):
        self.ensure_one()
        if (
            not self.operation_id.auto_create_lot
            or not self.operation_id.lot_sequence_id
            or self.lot_id
            or self.product_id.tracking == "none"
        ):
            return None

        self.lot_id = self.env["stock.lot"].create(self._prepare_rma_lot_vals())
        return self.lot_id
