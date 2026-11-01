# Copyright 2026 Aliaksandr Zubik <alexzub@tut.by> (https://artcloud.by)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from datetime import date, timedelta
from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestCurrencyRateUpdateNBRB(AccountTestInvoicingCommon):
    """Tests for NBRB currency rate provider."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Company = cls.env["res.company"]
        cls.CurrencyRate = cls.env["res.currency.rate"]
        cls.CurrencyRateProvider = cls.env["res.currency.rate.provider"]

        # Get currencies using XML IDs
        cls.currency_usd = cls.env.ref("base.USD")
        cls.currency_eur = cls.env.ref("base.EUR")
        # Get or create BYN currency
        cls.currency_byn = (
            cls.env["res.currency"]
            .with_context(active_test=False)
            .search([("name", "=", "BYN")], limit=1)
        )
        if cls.currency_byn:
            cls.currency_byn.active = True
        else:
            cls.currency_byn = cls.env["res.currency"].create(
                {"name": "BYN", "symbol": "Br", "active": True}
            )

        cls.company = cls.Company.create(
            {"name": "Test Company", "currency_id": cls.currency_byn.id}
        )
        cls.env.user.company_ids += cls.company
        cls.env.user.company_id = cls.company

        # Create NBRB provider
        cls.provider = cls.CurrencyRateProvider.create(
            {
                "service": "NBRB",
                "currency_ids": [
                    (4, cls.currency_usd.id),
                    (4, cls.currency_eur.id),
                ],
            }
        )

    def test_provider_service_available(self):
        """Test that NBRB service is available in selection."""
        services = dict(
            self.CurrencyRateProvider._fields["service"]._description_selection(
                self.env
            )
        )
        self.assertIn("NBRB", services)
        self.assertEqual(
            services["NBRB"], "National Bank of the Republic of Belarus (NBRB)"
        )

    def test_get_supported_currencies(self):
        """Test that supported currencies list is correct."""
        currencies = self.provider._get_supported_currencies()
        self.assertIsInstance(currencies, list)
        self.assertGreater(len(currencies), 25)
        # Check some major currencies
        self.assertIn("USD", currencies)
        self.assertIn("EUR", currencies)
        self.assertIn("RUB", currencies)
        self.assertIn("BYN", currencies)

    def _get_mock_nbrb_response(self):
        """Return mock NBRB API response."""
        return json.dumps(
            [
                {
                    "Cur_ID": 145,
                    "Date": "2026-02-13T00:00:00",
                    "Cur_Abbreviation": "USD",
                    "Cur_Scale": 1,
                    "Cur_Name": "Доллар США",
                    "Cur_OfficialRate": 3.2500,
                },
                {
                    "Cur_ID": 292,
                    "Date": "2026-02-13T00:00:00",
                    "Cur_Abbreviation": "EUR",
                    "Cur_Scale": 1,
                    "Cur_Name": "Евро",
                    "Cur_OfficialRate": 3.5200,
                },
                {
                    "Cur_ID": 298,
                    "Date": "2026-02-13T00:00:00",
                    "Cur_Abbreviation": "RUB",
                    "Cur_Scale": 100,
                    "Cur_Name": "Российских рублей",
                    "Cur_OfficialRate": 3.4800,
                },
            ]
        )

    @patch(
        "odoo.addons.currency_rate_update_nbrb.models.res_currency_rate_provider_nbrb.urlopen"
    )
    def test_obtain_rates_byn_base(self, mock_urlopen):
        """Test obtaining rates with BYN as base currency."""
        # Mock the API response
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.read.return_value.decode.return_value = (
            self._get_mock_nbrb_response()
        )

        date_from = date.today()
        date_to = date.today() + timedelta(days=1)

        rates = self.provider._obtain_rates("BYN", ["USD", "EUR"], date_from, date_to)

        # Check that rates were returned
        self.assertIsInstance(rates, dict)
        # Mock returns date 2026-02-13
        expected_date = "2026-02-13"
        self.assertIn(expected_date, rates)

        rate_date = rates[expected_date]
        self.assertIn("USD", rate_date)
        self.assertIn("EUR", rate_date)

        # Check that rates are inverted (1 BYN = X USD)
        usd_rate = float(rate_date["USD"])
        eur_rate = float(rate_date["EUR"])
        self.assertGreater(usd_rate, 0)
        self.assertGreater(eur_rate, 0)
        self.assertLess(usd_rate, 1)  # 1 BYN should be less than 1 USD

    @patch(
        "odoo.addons.currency_rate_update_nbrb.models.res_currency_rate_provider_nbrb.urlopen"
    )
    def test_obtain_rates_usd_base(self, mock_urlopen):
        """Test obtaining rates with USD as base currency."""
        # Mock the API response
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.read.return_value.decode.return_value = (
            self._get_mock_nbrb_response()
        )

        date_from = date.today()
        date_to = date.today() + timedelta(days=1)

        rates = self.provider._obtain_rates("USD", ["EUR", "BYN"], date_from, date_to)

        # Check that rates were returned
        self.assertIsInstance(rates, dict)
        # Mock returns date 2026-02-13
        expected_date = "2026-02-13"
        self.assertIn(expected_date, rates)

        rate_date = rates[expected_date]
        self.assertIn("EUR", rate_date)
        self.assertIn("BYN", rate_date)

        # Check that BYN rate is correct (should be ~3.25)
        byn_rate = float(rate_date["BYN"])
        self.assertGreater(byn_rate, 3.0)
        self.assertLess(byn_rate, 4.0)

    @patch(
        "odoo.addons.currency_rate_update_nbrb.models.res_currency_rate_provider_nbrb.urlopen"
    )
    def test_obtain_rates_api_error(self, mock_urlopen):
        """Test error handling when API fails."""
        # Mock API failure
        mock_urlopen.side_effect = Exception("Connection failed")

        date_from = date.today()
        date_to = date.today() + timedelta(days=1)

        with self.assertRaises(UserError) as context:
            self.provider._obtain_rates("BYN", ["USD"], date_from, date_to)

        self.assertIn("Error connecting to NBRB API", str(context.exception))

    @patch(
        "odoo.addons.currency_rate_update_nbrb.models.res_currency_rate_provider_nbrb.urlopen"
    )
    def test_obtain_rates_invalid_json(self, mock_urlopen):
        """Test error handling when API returns invalid JSON."""
        # Mock invalid JSON response
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.read.return_value.decode.return_value = "invalid json"

        date_from = date.today()
        date_to = date.today() + timedelta(days=1)

        with self.assertRaises(UserError) as context:
            self.provider._obtain_rates("BYN", ["USD"], date_from, date_to)

        self.assertIn("Exchange data format error", str(context.exception))

    @patch(
        "odoo.addons.currency_rate_update_nbrb.models.res_currency_rate_provider_nbrb.urlopen"
    )
    def test_obtain_rates_empty_response(self, mock_urlopen):
        """Test error handling when API returns empty list."""
        # Mock empty response
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.read.return_value.decode.return_value = "[]"

        date_from = date.today()
        date_to = date.today() + timedelta(days=1)

        with self.assertRaises(UserError) as context:
            self.provider._obtain_rates("BYN", ["USD"], date_from, date_to)

        self.assertIn("Exchange data format error", str(context.exception))

    @patch(
        "odoo.addons.currency_rate_update_nbrb.models.res_currency_rate_provider_nbrb.urlopen"
    )
    def test_obtain_rates_missing_currency(self, mock_urlopen):
        """Test handling of missing currency in API response."""
        # Mock response without requested currency
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.read.return_value.decode.return_value = json.dumps(
            [
                {
                    "Cur_ID": 145,
                    "Date": "2026-02-13T00:00:00",
                    "Cur_Abbreviation": "USD",
                    "Cur_Scale": 1,
                    "Cur_Name": "Доллар США",
                    "Cur_OfficialRate": 3.2500,
                }
            ]
        )

        date_from = date.today()
        date_to = date.today() + timedelta(days=1)

        # Request EUR which is not in the response
        # We expect a WARNING log for missing currency
        with self.assertLogs(
            "odoo.addons.currency_rate_update_nbrb.models.res_currency_rate_provider_nbrb",
            level="WARNING",
        ) as log_catcher:
            rates = self.provider._obtain_rates(
                "BYN", ["USD", "EUR"], date_from, date_to
            )

        # Verify the warning was logged
        self.assertTrue(
            any("EUR not found" in message for message in log_catcher.output)
        )

        # Mock returns date 2026-02-13
        expected_date = "2026-02-13"
        rate_date = rates[expected_date]
        # USD should be present
        self.assertIn("USD", rate_date)
        # EUR should be missing (logged as warning but not in result)
        # The method continues processing other currencies
