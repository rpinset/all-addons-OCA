# Copyright 2026 OCA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("-at_install", "post_install")
class TestL10nBGLanguageAndFields(TransactionCase):
    def test_bulgarian_language_available(self):
        lang = self.env["res.lang"].search([("code", "=", "bg_BG")], limit=1)
        if not lang:
            lang = self.env["res.lang"].create(
                {
                    "name": "Bulgarian",
                    "code": "bg_BG",
                    "iso_code": "bg",
                    "direction": "ltr",
                    "date_format": "%m/%d/%Y",
                    "time_format": "%H:%M:%S",
                    "thousands_sep": ",",
                    "decimal_point": ".",
                }
            )
        self.assertTrue(lang.active, "Bulgarian language should be active")

    def test_account_move_has_bg_fields(self):
        move_model = self.env["account.move"]
        self.assertIn("is_l10n_bg_record", move_model._fields)
        self.assertIn("l10n_bg_document_number", move_model._fields)
