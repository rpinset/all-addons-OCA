# Copyright 2025 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import tagged

from odoo.addons.sale_stock_prebook.tests.common import TestSaleStockPrebookCase


@tagged("post_install", "-at_install")
class TestSaleExceptionStockPrebook(TestSaleStockPrebookCase):
    def test_normal_prebook(self):
        self.sale.reserve_stock()
        self.assertTrue(self.sale.stock_is_reserved)
        self.assertEqual(len(self.sale._get_reservation_pickings()), 1)
        self.sale.release_reservation()
        self.assertFalse(self.sale.stock_is_reserved)
        self.assertFalse(self.sale._get_reservation_pickings())

    def test_action_confirm_no_release_with_exception(self):
        self.sale.reserve_stock()
        exception = self.env.ref("sale_exception.excep_no_zip").sudo()
        exception.active = True
        self.sale.partner_id.zip = False
        self.assertTrue(self.sale.detect_exceptions())
        self.assertTrue(self.sale.stock_is_reserved)
        self.assertEqual(len(self.sale._get_reservation_pickings()), 1)
        self.sale.action_confirm()
        self.assertTrue(self.sale.stock_is_reserved)
        self.assertEqual(len(self.sale._get_reservation_pickings()), 1)
