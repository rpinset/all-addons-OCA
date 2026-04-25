# Copyright 2018 - Today Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import tagged

from odoo.addons.point_of_sale.tests.common import TestPoSCommon


@tagged("post_install", "-at_install")
class TestPosPickingDelayed(TestPoSCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.config = cls.basic_config
        cls.product = cls.create_product("Product Test", cls.categ_basic, 5.0, 0.0)
        cls.QueueJob = cls.env["queue.job"]
        cls.PosOrder = cls.env["pos.order"]

    def _create_order(self, partner_id=False):
        self.open_new_session()
        orders = [self.create_ui_order_data([(self.product, 3)])]
        result = self.env["pos.order"].create_from_ui(orders)
        order = self.PosOrder.browse(result[0]["id"])
        return order

    def test_01_picking_delayed_enabled(self):
        # Enable feature
        self.basic_config.picking_creation_delayed = True

        order = self._create_order()

        self.assertEqual(
            order.picking_ids.id,
            False,
            "Creating order via UI should not generate a picking if"
            " feature is enabled",
        )

        # Test if a Queue Job has been generated
        func_string = "pos.order(%d,)._create_delayed_picking()" % (order.id)
        queues = self.QueueJob.search([("func_string", "=", func_string)])
        self.assertEqual(len(queues), 1, "Queue Job has not been created")

    def test_02_picking_delayed_disabled(self):
        # Disable feature
        self.basic_config.picking_creation_delayed = False

        order = self._create_order()

        self.assertNotEqual(
            order.picking_ids.id,
            False,
            "Creating order via UI should generate a picking if feature is disabled",
        )

        # Test if a Queue Job has not been generated
        func_string = "pos.order(%d,)._create_delayed_picking()" % (order.id)
        queues = self.QueueJob.search([("func_string", "=", func_string)])
        self.assertEqual(len(queues), 0, "Queue Job has been created")
