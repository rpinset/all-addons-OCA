from odoo.tests import TransactionCase


class TestSortedMoveLines(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.product_1 = cls.env.ref("product.product_product_3")
        cls.product_2 = cls.env.ref("product.product_product_4")
        cls.sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_1.id,
                            "product_uom_qty": 1,
                            "price_unit": 100,
                            "position": 3,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_2.id,
                            "product_uom_qty": 1,
                            "price_unit": 100,
                            "position": 1,
                        },
                    ),
                ],
            }
        )
        cls.picking_type = cls.env.ref("stock.picking_type_out")

    def test_sorted_moves_and_move_lines(self):
        """Ensure move lines in the delivery picking are sorted
        by sale line position."""
        self.sale_order.action_confirm()
        picking = self.sale_order.picking_ids[0]
        self.assertTrue(picking, "No picking created for sale order")
        picking.action_assign()
        picking.button_validate()
        lines = picking.get_delivery_report_lines()
        self.assertEqual(
            lines,
            lines.sorted(key=lambda line: line.move_id.sale_line_id.position),
            "Move lines are not sorted by sale line position",
        )
