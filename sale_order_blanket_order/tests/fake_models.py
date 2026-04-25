# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


# pylint: disable=consider-merging-classes-inherited
class FakeSaleOrder(models.Model):
    _inherit = "sale.order"

    blanket_reservation_strategy = fields.Selection(
        selection_add=[("fake", "For tests")],
        ondelete={"fake": "cascade"},
    )

    def _blanket_order_reserve_call_off_remaining_qty(self):
        # we need to override since our strategy is fake
        (
            _to_reserve,
            other_orders,
        ) = self._split_recrodset_for_reservation_strategy("fake")
        return super(
            FakeSaleOrder, other_orders
        )._blanket_order_reserve_call_off_remaining_qty()

    def _blanket_order_release_call_off_remaining_qty(self):
        # we need to override since our strategy is fake
        (
            _to_release,
            other_orders,
        ) = self._split_recrodset_for_reservation_strategy("fake")
        return super(
            FakeSaleOrder, other_orders
        )._blanket_order_release_call_off_remaining_qty()
