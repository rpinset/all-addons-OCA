# Copyright 2026 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def action_pos_session_close(
        self,
        balancing_account=False,
        amount_to_balance=0,
        bank_payment_method_diffs=None,
    ):
        res = super().action_pos_session_close(
            balancing_account,
            amount_to_balance,
            bank_payment_method_diffs,
        )
        # Trigger the sign-missed cron so cancelled or missed receipts are
        # signed right after closing without blocking or delaying the close.
        if any(
            s.config_id.asign_enabled and s.config_id.asign_state != "draft"
            for s in self
        ):
            self.env.ref("l10n_at_pos_rksv.pos_config_ir_cron")._trigger()
        return res
