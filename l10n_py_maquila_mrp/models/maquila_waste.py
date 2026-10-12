# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MaquilaWaste(models.Model):
    _name = "l10n_py.maquila.waste"
    _description = "Maquila Waste Management"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"

    name = fields.Char(compute="_compute_name", store=True)
    date = fields.Date(default=fields.Date.today, required=True)
    production_id = fields.Many2one(
        "mrp.production",
    )
    program_id = fields.Many2one(
        "l10n_py.maquila.program",
        required=True,
    )
    product_id = fields.Many2one(
        "product.product",
        required=True,
        string="Waste Product",
    )
    lot_id = fields.Many2one(
        "stock.lot",
        string="Lot/Serial",
    )
    quantity = fields.Float(
        required=True,
        digits="Product Unit of Measure",
    )
    waste_type = fields.Selection(
        [
            ("scrap", "Scrap"),
            ("byproduct", "Byproduct"),
            ("defective", "Defective"),
        ],
        required=True,
    )
    destination = fields.Selection(
        [
            ("destruction", "Destruction"),
            ("nationalization", "Nationalization"),
            ("reexport", "Re-export"),
        ],
        required=True,
    )
    state = fields.Selection(
        [
            ("pending", "Pending"),
            ("in_process", "In Process"),
            ("completed", "Completed"),
        ],
        default="pending",
        required=True,
        tracking=True,
    )
    justification = fields.Text()
    destruction_certificate = fields.Char(
        string="INTN Destruction Certificate",
    )
    seam_approval = fields.Char(
        string="MADES Dictamen",
        help="Environmental clearance (MADES, ex-SEAM per Ley 6123/2018)",
    )
    scrap_id = fields.Many2one(
        "stock.scrap",
    )
    nationalization_move_id = fields.Many2one(
        "account.move",
        string="Nationalization Entry",
    )
    company_id = fields.Many2one(
        related="program_id.company_id",
        store=True,
    )

    @api.depends("product_id", "date")
    def _compute_name(self):
        for rec in self:
            product = rec.product_id.name or _("Waste")
            rec.name = f"{product} - {rec.date or ''}"

    def action_process(self):
        self.write({"state": "in_process"})

    def action_complete(self):
        """Complete the waste disposal. For destruction, draft a stock scrap
        so the physical write-off is traceable; nationalization and re-export
        keep their own document references (entry / dispatch)."""
        for rec in self:
            if rec.destination == "destruction" and rec.product_id and not rec.scrap_id:
                rec.scrap_id = self.env["stock.scrap"].create(
                    {
                        "product_id": rec.product_id.id,
                        "scrap_qty": rec.quantity,
                        "product_uom_id": rec.product_id.uom_id.id,
                        "company_id": rec.company_id.id,
                        "origin": rec.name,
                    }
                )
        self.write({"state": "completed"})

    def action_pending(self):
        self.write({"state": "pending"})
