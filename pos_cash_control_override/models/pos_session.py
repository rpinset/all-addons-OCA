# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def try_cash_in_out(self, _type, amount, reason, extras):
        if not self.user_has_groups("account.group_account_invoice"):
            self = self.with_context(override_cash_control_permissions=True)
        return super().try_cash_in_out(_type, amount, reason, extras)

    def _get_pos_ui_pos_config(self, params):
        config = super()._get_pos_ui_pos_config(params)
        config["has_cash_move_permission"] = True
        return config
