# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase, TransactionCase, new_test_user, tagged


class TestBarcodeGs1UserAccess(TransactionCase):
    """The app reads the GS1 rules as whoever opens it.

    The Scanner menu is open to every internal user, so a plain employee must be
    able to read everything ``gs1_nomenclature.esm.js`` loads, with the same
    fields it asks for.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee = new_test_user(
            cls.env, login="barcode_gs1_employee", groups="base.group_user"
        )

    def test_employee_reads_the_gs1_nomenclature_and_rules(self):
        env = self.env(user=self.employee)
        company = env.company.read(["nomenclature_id"])
        self.assertIn("nomenclature_id", company[0])
        nomenclatures = env["barcode.nomenclature"].search_read(
            [("is_gs1_nomenclature", "=", True)],
            ["name", "is_gs1_nomenclature", "gs1_separator_fnc1"],
            limit=1,
        )
        self.assertTrue(nomenclatures)
        rules = env["barcode.rule"].search_read(
            [
                ("barcode_nomenclature_id", "=", nomenclatures[0]["id"]),
                ("encoding", "=", "gs1-128"),
            ],
            [
                "name",
                "sequence",
                "type",
                "pattern",
                "gs1_content_type",
                "gs1_decimal_usage",
                "associated_uom_id",
            ],
            order="sequence",
        )
        self.assertTrue(rules)
        # The unit a measure rule is expressed in is read through the rule.
        self.assertTrue(any(rule["associated_uom_id"] for rule in rules))


@tagged("post_install", "-at_install")
class TestBarcodeGs1Hoot(HttpCase):
    """Run the GS1 parser unit tests (``static/tests``) in the browser.

    The parsing itself is JS, so that suite is where it is actually covered. A
    Chrome/Chromium binary is required: without one the run is skipped, not
    passed.
    """

    def test_js(self):
        self.browser_js(
            "/web/tests?headless&loglevel=2&preset=desktop&filter=BarcodeGs1",
            "",
            "",
            login="admin",
            success_signal="[HOOT] Test suite succeeded",
            error_checker=lambda message: "[HOOT]" not in message,
        )
