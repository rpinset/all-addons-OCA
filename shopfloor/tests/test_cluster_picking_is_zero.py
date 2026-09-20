# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest import mock

from ..actions.inventory import InventoryAction
from .test_cluster_picking_base import ClusterPickingCommonCase

# pylint: disable=missing-return


def spy_confirm_empty():
    """Patch InventoryAction.confirm_empty to record its calls while still
    running it; use as a context manager, the mock is returned"""
    return mock.patch.object(
        InventoryAction,
        "confirm_empty",
        autospec=True,
        side_effect=InventoryAction.confirm_empty,
    )


class ClusterPickingIsZeroCase(ClusterPickingCommonCase):
    """Tests covering the /is_zero endpoint

    After a line has been scanned, if the location is empty, the
    client application is redirected to the "zero_check" state,
    where the user has to confirm or not that the location is empty.
    When the location is empty, there is nothing to do, but when it
    in fact not empty, a draft inventory must be created for the
    product so someone can verify.
    """

    @classmethod
    def setUpClassBaseData(cls, *args, **kwargs):
        super().setUpClassBaseData(*args, **kwargs)
        cls.batch = cls._create_picking_batch(
            [
                [
                    cls.BatchProduct(product=cls.product_a, quantity=10),
                    cls.BatchProduct(product=cls.product_b, quantity=10),
                ]
            ]
        )
        cls.picking = cls.batch.picking_ids
        cls._simulate_batch_selected(cls.batch)

        cls.line = cls.picking.move_line_ids[0]
        cls.next_line = cls.picking.move_line_ids[1]
        cls.line.location_id = cls.shelf1
        cls.next_line.location_id = cls.shelf2
        cls.bin1 = cls.env["stock.quant.package"].create({})
        cls._update_qty_in_location(
            cls.line.location_id, cls.line.product_id, cls.line.quantity
        )
        # we already scan and put the first line in bin1, at this point the
        # system see the location is empty and reach "zero_check"
        cls._set_dest_package_and_done(cls.line, cls.bin1)

    def source_qty(self, product, location):
        return sum(
            self.env["stock.quant"]._gather(product, location).mapped("quantity")
        )

    def test_is_zero_is_empty(self):
        """call /is_zero confirming it's empty"""
        # Source location holds the quantity to move
        available = self.source_qty(self.line.product_id, self.line.location_id)
        self.assertEqual(available, 10)
        with spy_confirm_empty() as confirm_empty:
            self.service.dispatch(
                "is_zero",
                params={
                    "picking_batch_id": self.batch.id,
                    "move_line_id": self.line.id,
                    "zero": True,
                },
            )
        confirm_empty.assert_called_once()
        # the remaining line is picked, then the batch is unloaded and validated
        self._set_dest_package_and_done(self.next_line, self.bin1)
        self.service.dispatch(
            "prepare_unload",
            params={"picking_batch_id": self.batch.id},
        )
        self.service.dispatch(
            "set_destination_all",
            params={
                "picking_batch_id": self.batch.id,
                "barcode": self.packing_location.barcode,
            },
        )
        self.assertEqual(self.picking.state, "done")
        # Check the source location is empty (no negative quants)
        available = self.source_qty(self.line.product_id, self.line.location_id)
        self.assertEqual(available, 0)

    def test_is_zero_is_not_empty(self):
        """call /is_zero not confirming it's empty"""
        response = self.service.dispatch(
            "is_zero",
            params={
                "picking_batch_id": self.batch.id,
                "move_line_id": self.line.id,
                "zero": False,
            },
        )
        quant = self.env["stock.quant"].search(
            [
                ("location_id", "=", self.line.location_id.id),
                ("product_id", "=", self.line.product_id.id),
                ("inventory_quantity_set", "=", True),
            ]
        )
        self.assertTrue(quant)
        self.assert_response(
            response,
            next_state="start_line",
            data=self._line_data(self.next_line),
            message={
                "message_type": "success",
                "body": f"{self.line.qty_picked} {self.line.product_id.display_name} put in {self.bin1.name}",  # noqa
            },
        )


class ClusterPickingIsZeroLotCase(ClusterPickingCommonCase):
    """Zero check on a location holding the product in a lot"""

    @classmethod
    def setUpClassBaseData(cls, *args, **kwargs):
        super().setUpClassBaseData(*args, **kwargs)
        cls.batch = cls._create_picking_batch(
            [[cls.BatchProduct(product=cls.product_a, quantity=10)]]
        )
        cls.picking = cls.batch.picking_ids
        cls._simulate_batch_selected(cls.batch, in_lot=True)
        cls.line = cls.picking.move_line_ids[0]
        cls.line.location_id = cls.shelf1
        cls.bin1 = cls.env["stock.quant.package"].create({})
        cls._update_qty_in_location(
            cls.line.location_id,
            cls.line.product_id,
            cls.line.quantity,
            lot=cls.line.lot_id,
        )
        cls._set_dest_package_and_done(cls.line, cls.bin1)

    def source_qty(self):
        return sum(
            self.env["stock.quant"]
            ._gather(self.line.product_id, self.line.location_id)
            .mapped("quantity")
        )

    def test_is_zero_is_empty_with_lot(self):
        self.assertTrue(self.line.lot_id)
        self.assertEqual(self.source_qty(), 10)
        with spy_confirm_empty() as confirm_empty:
            self.service.dispatch(
                "is_zero",
                params={
                    "picking_batch_id": self.batch.id,
                    "move_line_id": self.line.id,
                    "zero": True,
                },
            )
        confirm_empty.assert_called_once()
        self.assertEqual(confirm_empty.call_args.kwargs["lot"], self.line.lot_id)
        self.service.dispatch(
            "prepare_unload", params={"picking_batch_id": self.batch.id}
        )
        self.service.dispatch(
            "set_destination_all",
            params={
                "picking_batch_id": self.batch.id,
                "barcode": self.packing_location.barcode,
            },
        )
        self.assertEqual(self.picking.state, "done")
        # The lot quant must be emptied by the move, not by the zero check
        self.assertEqual(self.source_qty(), 0)
