from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _filter_out_blanket_carrier_lines(self):
        skip_filter = self.env.context.get("skip_blanket_carrier_filter")
        if not skip_filter:
            return self.filtered(lambda line: not line.is_delivery)
        return self

    @api.model
    def _match_lines_to_blanket(self, order_lines, blanket_lines):
        order_lines = order_lines._filter_out_blanket_carrier_lines()
        blanket_lines = blanket_lines._filter_out_blanket_carrier_lines()
        return super()._match_lines_to_blanket(order_lines, blanket_lines)

    def _forward_stock_rule_to_blanket_order(self, previous_product_uom_qty):
        # `is_delivery` call-off lines are excluded from blanket matching
        # by `_match_lines_to_blanket` above and therefore have no
        # `blanket_line_id` to forward the stock rule to.
        records = self._filter_out_blanket_carrier_lines()
        return super(SaleOrderLine, records)._forward_stock_rule_to_blanket_order(
            previous_product_uom_qty
        )
