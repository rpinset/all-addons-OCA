# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OutstandingStatementWizard(models.TransientModel):
    _inherit = "outstanding.statement.wizard"

    l10n_it_show_riba = fields.Boolean(
        string="Show RiBa",
        help="Add a column in the statements "
        "to identify the lines that come from RiBa.",
    )

    def _prepare_statement(self):
        values = super()._prepare_statement()
        values["l10n_it_show_riba"] = self.l10n_it_show_riba
        return values
