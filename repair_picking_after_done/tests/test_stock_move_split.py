from odoo.tests.common import TransactionCase


class TestStockMoveSplit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a product
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
            }
        )

        # Create a stock location
        cls.location = cls.env["stock.location"].create(
            {
                "name": "Test Location",
                "usage": "internal",
            }
        )

        # Create a repair order in 'draft' state
        cls.repair = cls.env["repair.order"].create(
            {
                "name": "Repair Order 1",
                "product_id": cls.product.id,
                "state": "draft",
            }
        )

        # Create a stock move linked to the repair order
        cls.stock_move = cls.env["stock.move"].create(
            {
                "name": "Stock Move for Repair Order 1",
                "product_id": cls.product.id,
                "product_uom_qty": 10.0,
                "product_uom": cls.product.uom_id.id,
                "repair_id": cls.repair.id,
                "state": "confirmed",
                "location_id": cls.location.id,
                "location_dest_id": cls.location.id,
            }
        )

    def test_split_move_with_incomplete_repair(self):
        """Ensure a stock move linked to an incomplete repair cannot be split"""
        result = self.stock_move._split(5.0)
        self.assertEqual(
            result, [], "Move should not split as the repair is not 'done'."
        )

    def test_split_move_with_completed_repair(self):
        """Ensure a stock move linked to a completed repair can be split"""
        self.repair.write({"state": "done"})
        result = self.stock_move._split(5.0)
        self.assertTrue(result, "Move should split as the repair is 'done'.")
