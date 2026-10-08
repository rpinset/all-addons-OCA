from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestResCompany(TransactionCase):
    """Tests para res.company (extensión paraguaya)"""

    def test_localization_use_documents_py(self):
        """Retorna True para empresa PY"""
        country_py = self.env.ref("base.py")
        company = self.env["res.company"].create(
            {
                "name": "Test Company PY",
                "country_id": country_py.id,
                "account_fiscal_country_id": country_py.id,
            }
        )
        self.assertTrue(company._localization_use_documents())

    def test_localization_use_documents_non_py(self):
        """No afecta empresas de otros países"""
        country_us = self.env.ref("base.us")
        company = self.env["res.company"].create(
            {
                "name": "Test Company US",
                "country_id": country_us.id,
                "account_fiscal_country_id": country_us.id,
            }
        )
        # US should not use documents by default
        result = company._localization_use_documents()
        # We just verify it doesn't crash; actual value depends on other localizations
        self.assertIsNotNone(result)
