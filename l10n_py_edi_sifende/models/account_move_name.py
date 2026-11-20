# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

# pylint: disable=consider-merging-classes-inherited
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    # el nombre contable (FE 00000027) es la secuencia del diario, no el número fiscal
    l10n_py_sifende_document_name = fields.Char(
        compute="_compute_l10n_py_sifende_document_name",
        string="Documento fiscal",
    )

    @api.depends(
        "state",
        "move_type",
        "company_id",
        "l10n_latam_document_type_id",
        "l10n_py_full_invoice_number",
    )
    def _compute_l10n_py_sifende_document_name(self):
        for move in self:
            move.l10n_py_sifende_document_name = (
                move.state == "posted"
                and move.l10n_py_full_invoice_number
                and move.l10n_latam_document_type_id
                and move._l10n_py_sifende_is_document()
                and f"{move.l10n_latam_document_type_id.name} "
                f"{move.l10n_py_full_invoice_number}"
            ) or False

    def _get_move_display_name(self, show_ref=False):
        display = super()._get_move_display_name(show_ref=show_ref)
        fiscal = self.l10n_py_sifende_document_name
        if fiscal and self.name and self.name != "/":
            return display.replace(self.name, fiscal, 1)
        return display
