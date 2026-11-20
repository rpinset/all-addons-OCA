# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AssociatedDocument(models.Model):
    _inherit = "l10n_py.associated.document"

    def _l10n_py_sifende_check_frozen(self, moves):
        for move in moves:
            if move._l10n_py_sifende_frozen():
                raise move._l10n_py_sifende_frozen_error(fiscal=True)

    @api.model_create_multi
    def create(self, vals_list):
        moves = self.env["account.move"].browse(
            [vals["move_id"] for vals in vals_list if vals.get("move_id")]
        )
        self._l10n_py_sifende_check_frozen(moves)
        return super().create(vals_list)

    def write(self, vals):
        self._l10n_py_sifende_check_frozen(self.move_id)
        return super().write(vals)

    def unlink(self):
        self._l10n_py_sifende_check_frozen(self.move_id)
        return super().unlink()
