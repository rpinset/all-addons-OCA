# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    l10n_py_maquila_program_id = fields.Many2one(
        "l10n_py.maquila.program",
        string="Maquila Program",
        compute="_compute_maquila_program",
        store=True,
        readonly=False,
        precompute=True,
        help="Defaults to the program of the bill of materials; can be set by "
        "hand for productions without a BoM.",
    )

    @api.depends("bom_id.l10n_py_maquila_program_id")
    def _compute_maquila_program(self):
        for production in self:
            production.l10n_py_maquila_program_id = (
                production.bom_id.l10n_py_maquila_program_id
            )
