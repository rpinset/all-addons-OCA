# Copyright 2026 Tecnativa - Juan Carlos Oñate
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def set_mandate(self):
        res = super().set_mandate()
        if (
            self.payment_mode_id.payment_method_id.mandate_required
            and self.partner_shipping_id.contact_mandate_id.state == "valid"
        ):
            self.mandate_id = self.partner_shipping_id.contact_mandate_id
        return res

    @api.onchange("partner_shipping_id")
    def _onchange_partner_shipping_id(self):
        res = super()._onchange_partner_shipping_id()
        self.set_mandate()
        return res
