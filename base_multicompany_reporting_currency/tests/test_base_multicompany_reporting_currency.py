# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from .common import Common


class TestBaseMulticompanyReportingCurrency(Common):
    def test_00_multicompany_reporting_currency(self):
        """Checks the correct multicompany reporting currency is retrieved"""
        ref = self.env.ref
        self._test_multicompany_reporting_currency(ref("base.USD").id, valid=True)
        self._test_multicompany_reporting_currency(ref("base.CHF").id, valid=True)
        self._test_multicompany_reporting_currency(ref("base.EUR").id, valid=True)

    def test_01_multicompany_reporting_currency_invalid(self):
        """Checks a warning is issued if the sys param is not a valid currency ID"""
        # Empty string (trimmed)
        self._test_multicompany_reporting_currency("", valid=False)
        # Empty string (blanks only)
        self._test_multicompany_reporting_currency("  ", valid=False)
        # Cannot convert to ``int``
        self._test_multicompany_reporting_currency("test", valid=False)
        # Not a real ID
        self._test_multicompany_reporting_currency(-1, valid=False)
        # No value (this will end up deleting the sys param itself)
        self._test_multicompany_reporting_currency(None, valid=False)

    def test_02_multicompany_reporting_currency_inheriting_model(self):
        """Checks the currency is updated on models inheriting from mixin"""
        eur = self.env.ref("base.EUR")
        usd = self.env.ref("base.USD")
        env_curr = self.env.company.currency_id

        # TEST INHERITING MODELS ARE RETRIEVED CORRECTLY
        # The result must be the same even if the method is called from inheriting
        # models
        mcrc_mixin = self.env["multicompany.reporting.currency.mixin"]
        fake_model = self.env["fake.model"]
        self.assertIn(
            fake_model,
            mcrc_mixin._get_multicompany_reporting_currency_inheriting_models(),
        )
        self.assertIn(
            fake_model,
            fake_model._get_multicompany_reporting_currency_inheriting_models(),
        )

        # TEST MIXIN DEFAULT VALUE
        # Set the multicompany reporting currency to EUR, then create 5 records per
        # model => all have EUR as multicompany reporting currency
        self._set_multicompany_reporting_currency_param(eur.id)
        fake_recs = fake_model.create([{}] * 5)
        self.assertRecordValues(
            fake_recs,
            [{"multicompany_reporting_currency_id": eur.id}] * 5,
        )

        # TEST SYS PARAM UPDATE IS REFLECTED ON RECORDS
        # Set the multicompany reporting currency to USD => all records will now have
        # USD as multicompany reporting currency
        self._set_multicompany_reporting_currency_param(usd.id)
        self.assertRecordValues(
            fake_recs,
            [{"multicompany_reporting_currency_id": usd.id}] * 5,
        )

        # TEST SYS PARAM DELETION IS REFLECTED ON RECORDS
        # Delete the sys param => all records will now have the user's currency
        self._set_multicompany_reporting_currency_param(None)
        self.assertRecordValues(
            fake_recs,
            [{"multicompany_reporting_currency_id": env_curr.id}] * 5,
        )

        # TEST SYS PARAM CREATION IS REFLECTED ON RECORDS
        # Recreate the sys param w/ USD => all records will now have USD
        self._set_multicompany_reporting_currency_param(usd.id)
        self.assertRecordValues(
            fake_recs,
            [{"multicompany_reporting_currency_id": usd.id}] * 5,
        )
