# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_py_maquila_program_id = fields.Many2one(
        "l10n_py.maquila.program",
        string="Maquila Program",
    )
    l10n_py_is_maquila_export = fields.Boolean(
        string="Maquila Export",
        compute="_compute_maquila_export",
        store=True,
    )

    @api.depends("l10n_py_maquila_program_id", "move_type")
    def _compute_maquila_export(self):
        for move in self:
            move.l10n_py_is_maquila_export = bool(
                move.l10n_py_maquila_program_id
                and move.move_type in ("out_invoice", "out_refund")
            )
