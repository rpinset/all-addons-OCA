# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    barcode_scan_state = fields.Selection(
        [("pending", "Pending"), ("done", "Done"), ("done_forced", "Done forced")],
        string="Scan State",
        default="pending",
        compute="_compute_barcode_scan_state",
        readonly=False,
        store=True,
    )

    @api.depends("qty_done", "product_uom_qty")
    def _compute_barcode_scan_state(self):
        for line in self:
            if line.qty_done >= line.product_uom_qty:
                line.barcode_scan_state = "done"
            else:
                line.barcode_scan_state = "pending"

    def _barcodes_process_line_to_unlink(self):
        self.qty_done = 0.0

    def action_barcode_detailed_operation_unlink(self):
        stock_moves = self.move_id
        self.unlink()
        stock_moves.barcode_backorder_action = "pending"
        # TODO: Any alternative to cover all cases without reassign?
        stock_moves._action_assign()
        # HACK: To force refresh wizard values
        wiz_barcode = self.env["wiz.stock.barcodes.read.picking"].browse(
            self.env.context.get("wiz_barcode_id", False)
        )
        wiz_barcode.with_context(
            skip_clean_values=True
        ).update_barcodes_wiz_after_changes()
