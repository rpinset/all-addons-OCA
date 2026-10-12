# Copyright 2026 KMEE
# The MrpBomLine net-quantity fields and helpers are derived from
# mrp_bom_line_net_qty, Copyright (C) 2023 GRAP (http://www.grap.coop),
# @author Quentin DUPONT.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    l10n_py_maquila_program_id = fields.Many2one(
        "l10n_py.maquila.program",
        string="Maquila Program",
    )
    l10n_py_intn_certified = fields.Boolean(
        string="INTN Certified",
    )
    l10n_py_intn_certificate = fields.Char(
        string="INTN Certificate Number",
    )
    l10n_py_intn_date = fields.Date(
        string="INTN Certification Date",
    )


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    # INTN technical coefficients (derived from GRAP's mrp_bom_line_net_qty):
    # product_qty (core, gross) = factor de requerimiento
    # product_qty_net = coeficiente neto
    # loss_percentage = coeficiente de desperdicio %
    product_qty_net = fields.Float(
        string="Net Quantity",
        help="Quantity after process (INTN net coefficient)",
        digits="Product Unit of Measure",
    )
    loss_percentage = fields.Float(
        string="Loss %",
        help="Percentage loss during process (INTN waste coefficient)",
        digits=(16, 2),
    )
    diff_product_qty_gross_net = fields.Float(
        string="Gross/Net Difference",
        digits="Product Price",
        compute="_compute_diff_product_qty_gross_net",
    )

    def calculate_qty_net_theoretical(self, product_qty_gross, loss_percentage):
        return (1 - loss_percentage / 100) * product_qty_gross

    @api.depends("product_qty", "product_qty_net", "loss_percentage")
    def _compute_diff_product_qty_gross_net(self):
        for bom_line in self:
            theoretical = self.calculate_qty_net_theoretical(
                bom_line.product_qty, bom_line.loss_percentage
            )
            bom_line.diff_product_qty_gross_net = round(
                bom_line.product_qty_net - theoretical, 2
            )

    def set_product_qty_net(self):
        for bom_line in self.filtered(lambda x: x.product_qty):
            bom_line.product_qty_net = self.calculate_qty_net_theoretical(
                bom_line.product_qty, bom_line.loss_percentage
            )

    def set_product_qty_gross(self):
        for bom_line in self.filtered(lambda x: x.product_qty_net):
            if bom_line.loss_percentage == 100:
                raise UserError(
                    _(
                        "Setting gross quantity with 100%% loss makes no sense.\n"
                        "Change this value."
                    )
                )
            bom_line.product_qty = bom_line.product_qty_net / (
                1 - bom_line.loss_percentage / 100
            )

    @api.onchange("product_qty")
    def _onchange_product_qty(self):
        for bom_line in self:
            bom_line.product_qty_net = bom_line.product_qty

    l10n_py_origin_type = fields.Selection(
        [
            ("temporary_admission", "Temporary Admission"),
            ("national_py", "National (Paraguay)"),
            ("national_mercosul", "National (Mercosul)"),
            ("imported", "Imported (Other)"),
        ],
        string="Origin Type",
    )
    l10n_py_origin_country = fields.Many2one(
        "res.country",
        string="Origin Country",
    )


class MaquilaProgramProduct(models.Model):
    _inherit = "l10n_py.maquila.program.product"

    bom_id = fields.Many2one(
        "mrp.bom",
        string="Bill of Materials",
    )
