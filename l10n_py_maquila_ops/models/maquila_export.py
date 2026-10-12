# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class MaquilaExport(models.Model):
    _name = "l10n_py.maquila.export"
    _description = "Maquila Export Dispatch"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_export desc"

    name = fields.Char(required=True, tracking=True)
    program_id = fields.Many2one(
        "l10n_py.maquila.program",
        required=True,
        tracking=True,
        domain="[('state', '=', 'active')]",
    )
    date_export = fields.Date(
        required=True,
        default=fields.Date.today,
        tracking=True,
    )
    incoterm = fields.Char()
    origin_certificate = fields.Char(
        string="Certificate of Origin",
        tracking=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("dispatched", "Dispatched"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )
    admission_ids = fields.Many2many(
        "l10n_py.maquila.admission",
        string="Source Admissions",
        help="Traceability to source temporary admissions",
    )
    line_ids = fields.One2many(
        "l10n_py.maquila.export.line",
        "export_id",
        string="Lines",
    )
    picking_ids = fields.One2many(
        "stock.picking",
        "l10n_py_maquila_export_id",
        string="Pickings",
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.ref("base.USD"),
    )
    company_id = fields.Many2one(
        related="program_id.company_id",
        store=True,
    )

    def action_confirm(self):
        for rec in self:
            if not rec.admission_ids:
                raise UserError(
                    _(
                        "Export must be linked to at least one source"
                        " admission for traceability."
                    )
                )
        self.write({"state": "confirmed"})

    def action_dispatch(self):
        self.write({"state": "dispatched"})

    def action_draft(self):
        self.write({"state": "draft"})


class MaquilaExportLine(models.Model):
    _name = "l10n_py.maquila.export.line"
    _description = "Maquila Export Line"

    export_id = fields.Many2one(
        "l10n_py.maquila.export",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        "product.product",
        required=True,
    )
    quantity = fields.Float(
        required=True,
        digits="Product Unit of Measure",
    )
    uom_id = fields.Many2one(
        "uom.uom",
        string="Unit of Measure",
    )
    currency_id = fields.Many2one(
        related="export_id.currency_id",
    )
    fob_value = fields.Monetary(
        string="FOB Value",
    )
