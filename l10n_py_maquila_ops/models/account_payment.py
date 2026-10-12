# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    l10n_py_maquila_program_id = fields.Many2one(
        "l10n_py.maquila.program",
        string="Maquila Program",
    )
    l10n_py_remittance_type = fields.Selection(
        [
            ("dividends", "Dividends"),
            ("royalties", "Royalties"),
            ("interest", "Interest"),
        ],
        string="Remittance Type",
    )
    l10n_py_is_maquila_exempt = fields.Boolean(
        string="Maquila Exempt",
        compute="_compute_maquila_exempt",
    )

    @api.depends("l10n_py_maquila_program_id", "l10n_py_maquila_program_id.state")
    def _compute_maquila_exempt(self):
        for payment in self:
            payment.l10n_py_is_maquila_exempt = bool(
                payment.l10n_py_maquila_program_id
                and payment.l10n_py_maquila_program_id.state == "active"
            )
