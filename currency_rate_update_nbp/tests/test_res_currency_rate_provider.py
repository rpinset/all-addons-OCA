# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from unittest import mock

from odoo.tests import TransactionCase, tagged

from . import response_data


def mocked_requests_get(*args, **kwargs):
    """Return mocked data"""
    magic_mock = mock.MagicMock()
    magic_mock.content = bytes(response_data.response, encoding="utf-8")
    return magic_mock


@tagged("post_install", "-at_install")
class TestResCurrencyRateProvider(TransactionCase):
    @classmethod
    def setUpClass(cls):
        """Initial common set up class for all tests."""
        super().setUpClass()

        cls.ResCompany = cls.env["res.company"]
        cls.ResCurrencyRateProvider = cls.env["res.currency.rate.provider"]
        cls.ResCurrencyRateUpdateWizard = cls.env["res.currency.rate.update.wizard"]

        cls.currency_eur = cls.env.ref("base.EUR")
        cls.currency_usd = cls.env.ref("base.USD")
        cls.currency_pln = cls.env.ref("base.PLN")
        cls.currency_pln.active = True
        cls.currencies = cls.currency_eur + cls.currency_usd + cls.currency_pln

        cls.company = cls.ResCompany.create(
            {
                "name": "Test Company",
                "currency_id": cls.currency_eur.id,
            }
        )
        cls.provider_nbp = cls.ResCurrencyRateProvider.with_company(cls.company).create(
            {
                "service": "NBP",
                "currency_ids": cls.currencies.ids,
            }
        )

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_obtain_rates_nbp_eur(self, *args):
        """Check syncing currency with company's currency eur"""
        # before syncing confirm that rates are 1
        self.assertEqual(
            3, sum(self.currencies.with_company(self.company).mapped("rate"))
        )

        # sync rates
        self.ResCurrencyRateUpdateWizard.with_company(self.company).create(
            {
                "provider_ids": self.provider_nbp.ids,
            }
        ).action_update()

        # check that currencies were synced properly
        self.assertEqual(
            1.0, round(self.currency_eur.with_company(self.company).rate, 4)
        )
        self.assertEqual(
            1.0642, round(self.currency_usd.with_company(self.company).rate, 4)
        )
        self.assertEqual(
            4.6925, round(self.currency_pln.with_company(self.company).rate, 4)
        )

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_obtain_rates_nbp_pln(self, *args):
        """Check syncing currency with company's currency pln"""
        # change company's currency to pln
        self.company.currency_id = self.currency_pln

        # before syncing confirm that rates are 1
        self.assertEqual(
            3, sum(self.currencies.with_company(self.company).mapped("rate"))
        )

        # sync rates
        self.ResCurrencyRateUpdateWizard.with_company(self.company).create(
            {
                "provider_ids": self.provider_nbp.ids,
            }
        ).action_update()

        # check that currencies were synced properly
        self.assertEqual(
            0.2131, round(self.currency_eur.with_company(self.company).rate, 4)
        )
        self.assertEqual(
            0.2268, round(self.currency_usd.with_company(self.company).rate, 4)
        )
        self.assertEqual(
            1.0, round(self.currency_pln.with_company(self.company).rate, 4)
        )
