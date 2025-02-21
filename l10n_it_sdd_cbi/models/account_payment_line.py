# Copyright 2024 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountPaymentLineInherit(models.Model):
    _inherit = "account.payment.line"

    def _prepare_account_payment_vals(self):
        vals = super()._prepare_account_payment_vals()
        if self.order_id.payment_method_id.code.startswith("cbi_sdd_italy"):
            today = fields.Date.context_today(self)

            if self.order_id.date_prefered == "due":
                requested_date = self[:1].ml_maturity_date or self[:1].date or today
            elif self.order_id.date_prefered == "fixed":
                requested_date = self.order_id.date_scheduled or today
            else:
                requested_date = fields.Date.context_today(self)
            vals["date"] = requested_date
        return vals
