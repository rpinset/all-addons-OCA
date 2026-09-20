# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from .common import CommonCase


class TestInventory(CommonCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with cls.work_on_actions(cls) as work:
            cls.inventory = work.component(usage="inventory")
        cls.location = cls.shelf1
        cls.product = (
            cls.env["product.product"]
            .sudo()
            .create({"name": "screw", "is_storable": True})
        )
        cls.quant_model = cls.env["stock.quant"]
        cls.quants_before = cls.quant_model.browse()

    @classmethod
    def _update_quants(cls):
        cls.quants_before = cls.quant_model._gather(cls.product, cls.location)

    @classmethod
    def _get_new_quants(cls):
        return cls.quant_model._gather(cls.product, cls.location) - cls.quants_before

    def assert_inventory_quant_zero(self, quants):
        for quant in quants:
            self.assertEqual(quant.inventory_quantity, 0)
            self.assertTrue(quant.inventory_quantity_set)

    @classmethod
    def _add_stock_to_product(cls):
        """Set the stock quantity of the product."""
        values = {
            "product_id": cls.product.id,
            "location_id": cls.location.id,
            "inventory_quantity": 10.0,
        }
        cls.quant_model.sudo().with_context(inventory_mode=True).create(
            values
        )._apply_inventory()
        cls._update_quants()

    def test_no_stock_confirm_empty(self):
        # there's no stock and no draft inventory
        # confirm_empty should auto-validate the zero inventory
        self.inventory.confirm_empty(self.location, self.product)
        quants = self.quant_model._gather(self.product, self.location)
        self.assertEqual(len(quants), 1)
        self.assertFalse(self.inventory._inventory_exists(self.location, self.product))
        self.assertEqual(quants.quantity, 0)
        self.assertFalse(quants.inventory_quantity_set)

    def test_no_stock_confirm_not_empty(self):
        # there's no stock
        # confirm not empty should create a new inventory quand with qty 1
        self.inventory.confirm_not_empty(self.location, self.product)
        new_quants = self._get_new_quants()
        self.assertEqual(len(new_quants), 1)
        self.assert_inventory_quant_zero(new_quants)

    def test_stock_confirm_empty(self):
        # There's stock
        self._add_stock_to_product()
        # confirm_empty should set inventory_qty to 0 on existing quants
        self.inventory.confirm_empty(self.location, self.product)
        new_quants = self._get_new_quants()
        self.assertFalse(new_quants)
        self.assertEqual(self.quants_before.inventory_quantity, 0)
        self.assertFalse(self.quants_before.inventory_quantity_set)

    def test_stock_confirm_not_empty(self):
        # There's stock
        self._add_stock_to_product()
        # confirm_not_empty should set inventory qty to 1 on existing quants
        self.inventory.confirm_not_empty(self.location, self.product)
        new_quants = self._get_new_quants()
        self.assertFalse(new_quants)
        self.assert_inventory_quant_zero(self.quants_before)


class TestInventoryConfirmEmptyOpenLine(CommonCase):
    """confirm_empty while the move line that emptied the location is open

    The zero check is triggered before the picked move lines are done, so the
    quants still hold the picked quantity. Confirming the location is empty
    must not create an adjustment: the move line will take that quantity.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with cls.work_on_actions(cls) as work:
            cls.inventory = work.component(usage="inventory")
        cls.location = cls.shelf1
        cls.picking_type = cls.env.ref("stock.picking_type_out")
        cls.product = (
            cls.env["product.product"]
            .sudo()
            .create({"name": "screw", "is_storable": True})
        )

    def _source_qty(self):
        quants = self.env["stock.quant"]._gather(self.product, self.location)
        return sum(quants.mapped("quantity"))

    def _pick_all_and_confirm_empty(self, lot=None, package=None):
        self._update_qty_in_location(
            self.location, self.product, 10, lot=lot, package=package
        )
        picking = self._create_picking(lines=[(self.product, 10)])
        picking.action_assign()
        line = picking.move_line_ids
        self.assertEqual(line.location_id, self.location)
        line.write({"qty_picked": 10, "picked": True})
        self.inventory.confirm_empty(
            self.location, self.product, package=line.package_id, lot=line.lot_id
        )
        # nothing moved yet: the picked quantity is still in the location
        self.assertEqual(self._source_qty(), 10)
        self.assertFalse(
            self.env["stock.move"]
            .search([("product_id", "=", self.product.id), ("is_inventory", "=", True)])
            .filtered(lambda m: m.quantity)
        )
        picking._action_done()
        self.assertEqual(picking.state, "done")
        self.assertEqual(self._source_qty(), 0)

    def test_confirm_empty_open_line(self):
        self._pick_all_and_confirm_empty()

    def test_confirm_empty_open_line_lot(self):
        lot = (
            self.env["stock.lot"]
            .sudo()
            .create({"product_id": self.product.id, "name": "LOT1"})
        )
        self._pick_all_and_confirm_empty(lot=lot)

    def test_confirm_empty_open_line_package(self):
        package = self.env["stock.quant.package"].create({})
        self._pick_all_and_confirm_empty(package=package)
