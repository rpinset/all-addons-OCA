# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.exceptions import UserError
from odoo.tools import mute_logger

from odoo.addons.printing_auto_base.tests.common import (
    TestPrintingAutoCommon,
    patch_print_document,
)


class TestAutoPrinting(TestPrintingAutoCommon):
    @classmethod
    def setUpReportAndRecord(cls):
        cls.report_ref = "mrp.action_report_production_order"
        cls.record = cls.env.ref("mrp.mrp_production_4")

    def setUp(self):
        # Note: Using setUpClass, cls.record.picking_type_id.auto_printing_ids
        # is reset on each test making them fail
        super().setUp()
        self.printing_auto = self._create_printing_auto_attachment()
        self._create_attachment(self.record, self.data, "1")
        self.record.picking_type_id.auto_printing_ids |= self.printing_auto

    @patch_print_document()
    def test_button_mark_done_printing_auto(self):
        self.printing_auto.printer_id = self.printer_1
        self.record.button_mark_done()
        self.assertFalse(self.record.printing_auto_error)
        kwargs = {"report": None, "content": self.data, "printer": self.printer_1}
        self.printer_1.print_document.assert_called_once_with(**kwargs)

    @patch_print_document()
    def test_button_mark_done_printing_error_log(self):
        with mute_logger("odoo.addons.printing_auto_base.models.printing_auto_mixin"):
            self.record.button_mark_done()
        self.assertTrue(self.record.printing_auto_error)
        self.printer_1.print_document.assert_not_called()

    @patch_print_document()
    def test_button_mark_done_printing_error_raise(self):
        self.printing_auto.action_on_error = "raise"
        with self.assertRaises(UserError):
            self.record.button_mark_done()
        self.printer_1.print_document.assert_not_called()
