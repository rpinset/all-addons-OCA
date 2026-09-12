# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form

from odoo.addons.route_planning_rma.tests.common import TestRoutePlanningRmaCommon


class TestRoutePlanningRmaSaleCommon(TestRoutePlanningRmaCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create sale order
        order_form = Form(cls.env["sale.order"])
        order_form.partner_id = cls.partner_1
        with order_form.order_line.new() as line_form:
            line_form.product_id = cls.product_a
        cls.order = order_form.save()

    @classmethod
    def _rma_sale_wizard(cls, order):
        wizard_id = order.action_create_rma()["res_id"]
        wizard = cls.env["sale.order.rma.wizard"].browse(wizard_id)
        wizard.operation_id = cls.env.ref("rma.rma_operation_replace")
        return wizard
