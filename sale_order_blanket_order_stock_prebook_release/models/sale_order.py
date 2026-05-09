# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import timedelta

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    blanket_move_date_priority = fields.Datetime(
        string="Move Date Priority",
        help="Date priority for the moves of the order.",
    )

    commitment_date = fields.Datetime(inverse="_inverse_commitment_date")

    blanket_validity_start_date = fields.Date(
        inverse="_inverse_blanket_validity_start_date"
    )

    def action_confirm(self):
        self.flush_recordset()
        self._set_blanket_move_date_priority()
        return super().action_confirm()

    def _set_blanket_move_date_priority(self):
        """
        Compute the move date priority for the blanket orders.

        The move date priority for blanket orders is the validity start date of
        the blanket order incremented by the position of the order according to
        the confirmation date by blanket_validity_start_date.
        This method is called at the start of the confirmation process.
        """

        # ensure validity_start_date is set otherwise sql query will fail
        blankets = self.filtered(
            lambda o: o.order_type == "blanket" and o.blanket_validity_start_date
        )
        # we need to query the count of confirmed blanket orders for each
        # blanket_validity_start_date
        if not blankets:
            return

        start_dates = blankets.mapped("blanket_validity_start_date")
        groupby_key = "blanket_validity_start_date:day"
        groups = self.env["sale.order"]._read_group(
            domain=[
                ("order_type", "=", "blanket"),
                ("state", "in", ("sale", "done")),
                ("blanket_validity_start_date", "in", start_dates),
            ],
            fields=["order_count:count(id)"],
            groupby=[groupby_key],
        )
        count_per_date = {
            fields.Date.to_date(g["__range"][groupby_key]["from"]): g["order_count"]
            for g in groups
        }
        for order in blankets.sorted("create_date"):
            start_date = order.blanket_validity_start_date
            order_position = count_per_date.get(start_date, 0)
            order.blanket_move_date_priority = fields.Datetime.to_datetime(
                start_date
            ) + timedelta(seconds=order_position)
            count_per_date[start_date] = order_position + 1

    def _inverse_commitment_date(self):
        blanket_orders = self.filtered(
            lambda o: o.order_type == "blanket" and o.state != "draft"
        )
        blanket_orders = blanket_orders.with_context(from_inverse_commitment_date=True)

        # Ensure we do not get back into the "_inverse_blanket_validity_start_date"
        # since this would trigger "_set_blanket_move_date_priority" and this
        # would mess with the date priority
        for blanket_order in blanket_orders:
            blanket_order.write(
                {"blanket_validity_start_date": blanket_order.commitment_date}
            )

    def _inverse_blanket_validity_start_date(self):
        """
        Update the commitment date to the new start date +
        refresh related ongoing out moves date priority
        """
        blanket_orders = self.filtered(
            lambda o: o.order_type == "blanket" and o.state != "draft"
        )
        if not blanket_orders or blanket_orders._context.get(
            "from_inverse_commitment_date"
        ):
            return

        for order in blanket_orders:
            order.commitment_date = order.blanket_validity_start_date

        blanket_orders._set_blanket_move_date_priority()

        out_moves = self.env["stock.move"].search(
            [
                ("sale_line_id.order_id", "in", blanket_orders.ids),
                ("state", "not in", ("done", "cancel")),
                ("picking_type_id.code", "=", "outgoing"),
            ]
        )
        for move in out_moves:
            move.date_priority = move.sale_line_id.order_id.blanket_move_date_priority
