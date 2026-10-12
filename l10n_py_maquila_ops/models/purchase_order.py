# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    l10n_py_maquila_program_id = fields.Many2one(
        "l10n_py.maquila.program",
        string="Maquila Program",
    )

    @api.onchange("l10n_py_maquila_program_id")
    def _onchange_maquila_program(self):
        if self.l10n_py_maquila_program_id:
            # Set fiscal position for temporary admission
            fp = self.env.ref(
                "l10n_py_maquila_ops.fiscal_position_maquila_admission",
                raise_if_not_found=False,
            )
            if fp:
                self.fiscal_position_id = fp


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    l10n_py_origin_type = fields.Selection(
        [
            ("temporary_admission", "Temporary Admission"),
            ("national_py", "National (Paraguay)"),
            ("national_mercosul", "National (Mercosul)"),
            ("imported", "Imported (Other)"),
        ],
        string="Origin Type",
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if self.env.context.get("default_order_id"):
            order = self.env["purchase.order"].browse(
                self.env.context["default_order_id"]
            )
            if order.l10n_py_maquila_program_id:
                defaults["l10n_py_origin_type"] = "temporary_admission"
        return defaults
