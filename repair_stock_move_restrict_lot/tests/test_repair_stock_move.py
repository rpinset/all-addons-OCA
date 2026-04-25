from odoo.tests import common


class TestRepairStockMove(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestRepairStockMove, cls).setUpClass()
        # Models
        cls.StockProductionLot = cls.env["stock.production.lot"]
        cls.StockQuant = cls.env["stock.quant"]
        # Partners
        cls.res_partner_1 = cls.env["res.partner"].create({"name": "Wood Corner"})

        cls.env.user.groups_id |= cls.env.ref("stock.group_stock_user")

        # setup for the tests with lots
        # we create several lots qith qty
        # we want to check the system will get the correct lot
        cls.product_lot = cls.env["product.product"].create(
            {
                "name": "Acoustic Magic Bloc",
                "list_price": 2950.0,
                "type": "product",
                "tracking": "serial",
            }
        )
        cls.lot = cls.StockProductionLot.create(
            {
                "product_id": cls.product_lot.id,
                "name": "Lot A",
                "company_id": cls.env.company.id,
            }
        )
        cls.lot2 = cls.lot.copy({"name": "Lot B"})
        cls.lot3 = cls.lot.copy({"name": "Lot C"})
        cls.stock_location_stock = cls.env.ref("stock.stock_location_stock")
        cls.StockQuant.create(
            {
                "location_id": cls.stock_location_stock.id,
                "product_id": cls.product_lot.id,
                "lot_id": cls.lot.id,
                "inventory_quantity": 1,
            }
        ).action_apply_inventory()
        cls.StockQuant.create(
            {
                "location_id": cls.stock_location_stock.id,
                "product_id": cls.product_lot.id,
                "lot_id": cls.lot2.id,
                "inventory_quantity": 1,
            }
        ).action_apply_inventory()
        cls.StockQuant.create(
            {
                "location_id": cls.stock_location_stock.id,
                "product_id": cls.product_lot.id,
                "lot_id": cls.lot3.id,
                "inventory_quantity": 1,
            }
        ).action_apply_inventory()
        cls.repair_with_lot = cls.env["repair.order"].create(
            {
                "invoice_method": "none",
                "user_id": False,
                "product_id": cls.product_lot.id,
                "product_uom": cls.env.ref("uom.product_uom_unit").id,
                "location_id": cls.stock_location_stock.id,
                "lot_id": cls.lot3.id,
                "partner_id": cls.res_partner_1.id,
            }
        )

    def test_stock_move_lot_reservation(self):
        self.repair_with_lot.action_validate()
        # Start Repair
        self.repair_with_lot.action_repair_start()
        # check stock move status and lot_id
        for move in self.repair_with_lot.mapped("stock_move_ids"):
            self.assertEqual(
                move.state,
                "assigned",
                "Generated stock move state should be assigned",
            )
            self.assertEqual(
                move.move_line_ids.lot_id,
                self.repair_with_lot.lot_id,
                "Generated stock move lot_id should be the same as repair order",
            )
