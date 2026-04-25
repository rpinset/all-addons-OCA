# Copyright 2024 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestRepairTypeProductDestination(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.stock_location = cls.env["stock.location"].create(
            {
                "name": "Stock Location",
                "usage": "internal",
            }
        )

        cls.product_destination_location = cls.env["stock.location"].create(
            {
                "name": "Product Destination Location",
                "usage": "internal",
            }
        )

        cls.warehouse = cls.env["stock.warehouse"].create(
            {
                "name": "Test Warehouse",
                "code": "TW",
                "lot_stock_id": cls.stock_location.id,
            }
        )

        cls.picking_type = cls.env["stock.picking.type"].create(
            {
                "name": "Repair Operation Type",
                "code": "repair_operation",
                "warehouse_id": cls.warehouse.id,
                "default_location_src_id": cls.stock_location.id,
                "default_product_location_dest_id": cls.product_destination_location.id,
                "sequence_code": "RO",
            }
        )

        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
            }
        )

        cls.repair_order = cls.env["repair.order"].create(
            {
                "name": "Test Repair Order",
                "picking_type_id": cls.picking_type.id,
                "product_id": cls.product.id,
            }
        )

    def test_product_location_dest_id_computation(self):
        """Test that product_location_dest_id is correctly computed."""
        self.repair_order._compute_product_location_dest_id()
        self.assertEqual(
            self.repair_order.product_location_dest_id,
            self.picking_type.default_product_location_dest_id,
            "The product_location_dest_id should be set to the default location.",
        )

    def test_default_product_location_dest_id_computation(self):
        """Test the computation of default_product_location_dest_id in picking type."""
        self.picking_type._compute_default_product_location_dest_id()

        self.assertEqual(
            self.picking_type.default_product_location_dest_id,
            self.picking_type.warehouse_id.lot_stock_id,
            "The default_product_location_dest_id should be set to the "
            "stock location when the code is 'repair_operation'.",
        )
