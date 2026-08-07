# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.fields import Domain


class AccountPaymentLineCreate(models.TransientModel):
    _inherit = "account.payment.line.create"

    date_type = fields.Selection(
        selection_add=[("discount_due_date", "Discount Due Date")],
        ondelete={"discount_due_date": "cascade"},
    )
    cash_discount_date = fields.Date(
        default=lambda _: fields.Date.today(),
        help="Search lines with a discount due date which is posterior to "
        "the selected date.",
    )

    def _prepare_move_line_domain(self):
        self.ensure_one()
        domain = super()._prepare_move_line_domain()
        if self.date_type == "discount_due_date":
            domain &= Domain("discount_date", ">=", self.cash_discount_date)
        return domain
