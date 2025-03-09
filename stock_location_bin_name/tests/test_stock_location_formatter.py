from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.stock_location_bin_name.models.stock_location import PartialFormatter


class TestPartialFormatter(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.formatter = PartialFormatter()

    def test_partial_formatter_missing_field(self):
        """Test PartialFormatter when a field is missing"""
        test_data = {"existing": "value"}
        result = self.formatter.format("{existing}-{missing}", **test_data)
        self.assertEqual(result, "value-~")

    def test_partial_formatter_invalid_format(self):
        """Test PartialFormatter when format specification is invalid"""
        test_data = {"number": "not_a_number"}
        result = self.formatter.format("{number:d}", **test_data)
        self.assertEqual(result, "!")

    def test_partial_formatter_raise_error(self):
        """Test PartialFormatter when bad_fmt is None to raise the error"""
        formatter = PartialFormatter(bad_fmt=None)
        test_data = {"number": "not_a_number"}
        with self.assertRaises(ValueError):
            formatter.format("{number:d}", **test_data)
