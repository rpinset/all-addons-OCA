# Copyright 2026 Camptocamp (https://www.camptocamp.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields

from .common import PromiseReleaseCommonCase


class TestNeedReleaseNonDelivery(PromiseReleaseCommonCase):
    """Decreasing the demand of a delivery must not create a transfer to release.

    When the demand of an outgoing move is decreased, Odoo creates a move with a
    negative quantity. Either it is merged into the delivery it decreases, or,
    when the delivery can no longer be amended, it is turned into a return, i.e.
    an incoming transfer. Such a transfer is not a delivery and must therefore
    never be flagged as needing a release.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wh.delivery_route_id.available_to_promise_defer_pull = True
        cls._update_qty_in_location(cls.loc_bin1, cls.product1, 20.0)
        pickings = cls._create_picking_chain(cls.wh, [(cls.product1, 10.0)])
        cls.ship_picking = cls._out_picking(pickings)
        cls.ship_move = cls.ship_picking.move_ids
        # sanity check on the fixture: a deferred delivery needs a release
        assert cls.ship_move.need_release

    def _decrease_demand(self, qty, context=None):
        """Decrease the demand of the delivery by ``qty`` (a positive number).

        Reproduces what a sale order line does when its quantity is lowered: it
        runs a procurement with a negative quantity in the same procurement
        group. Returns the moves created by that procurement, if any.
        """
        last_move = self.env["stock.move"].search([], order="id desc", limit=1)
        group = self.env["procurement.group"].with_context(**(context or {}))
        values = {
            "company_id": self.wh.company_id,
            "group_id": self.group,
            "date_planned": fields.Datetime.now(),
            "warehouse_id": self.wh,
        }
        group.run(
            [
                group.Procurement(
                    self.product1,
                    -qty,
                    self.product1.uom_id,
                    self.loc_customer,
                    "TEST",
                    "TEST",
                    self.wh.company_id,
                    values,
                )
            ]
        )
        return self.env["stock.move"].search([("id", ">", last_move.id)])

    def _make_delivery_not_amendable(self):
        """Release the delivery and print its picking transfer.

        A printed picking transfer means the goods are being collected, so the
        delivery can no longer be unreleased, hence no longer be amended.
        """
        self.ship_move.release_available_to_promise()
        self._prev_picking(self.ship_picking).printed = True
        self.assertFalse(self.ship_move.need_release)
        self.assertFalse(self.ship_move.unrelease_allowed)

    def test_decrease_amendable_delivery_is_merged(self):
        """The fix must not break the normal case: the delivery is amended."""
        extra_moves = self._decrease_demand(3.0)
        self.assertFalse(extra_moves)
        self.assertEqual(self.ship_move.product_uom_qty, 7.0)
        self.assertTrue(self.ship_move.need_release)

    def test_decrease_non_amendable_delivery_creates_return_without_need_release(self):
        """The return created by the decrease must not need a release."""
        self._make_delivery_not_amendable()

        return_move = self._decrease_demand(3.0)

        self.assertEqual(len(return_move), 1)
        self.assertEqual(return_move.product_uom_qty, 3.0)
        self.assertNotEqual(return_move.picking_type_id.code, "outgoing")
        self.assertFalse(return_move.need_release)
        self.assertFalse(return_move.picking_id.need_release)

    def test_decrease_non_amendable_delivery_bug_without_the_fix(self):
        """Same case with the fix disabled: proves the fix is what solves it.

        Without the check in ``StockMove._action_confirm``, the return keeps the
        ``need_release`` flag it was given while it still was a delivery move,
        and shows up in the release views. That is the reported bug.
        """
        self._make_delivery_not_amendable()

        return_move = self._decrease_demand(
            3.0, context={"skip_need_release_non_delivery_check": True}
        )

        self.assertEqual(len(return_move), 1)
        self.assertNotEqual(return_move.picking_type_id.code, "outgoing")
        self.assertTrue(return_move.need_release)
