# Copyright 2026 andyengit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime
from zoneinfo import ZoneInfo

import requests

from odoo import fields
from odoo.tests import tagged
from odoo.tools import mute_logger

from odoo.addons.account.tests.common import AccountTestInvoicingCommon

CARACAS_TZ = ZoneInfo("America/Caracas")

BCV_HTML = b"""
<html><body>
<div id="dolar"><div><div><div></div><div><strong>36,50</strong></div></div></div></div>
<div id="euro"><div><div><div></div><div><strong>40,00</strong></div></div></div></div>
<div id="yuan"><div><div><div></div><div><strong>5,00</strong></div></div></div></div>
<div id="lira"><div><div><div></div><div><strong>1,10</strong></div></div></div></div>
<div id="rublo"><div><div><div></div><div><strong>0,40</strong></div></div></div></div>
</body></html>
"""


@tagged("post_install", "-at_install")
class TestResCurrencyRateProviderBCV(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bcv_status_code = 200
        cls.bcv_content = BCV_HTML
        cls.bcv_raise = None
        cls.ves = cls.env.ref("base.VES")
        cls.usd = cls.env.ref("base.USD")
        cls.eur = cls.env.ref("base.EUR")
        (cls.ves | cls.usd | cls.eur).write({"active": True})
        cls.company = cls.env.company
        cls.company.currency_id = cls.ves
        cls.provider = cls.env["res.currency.rate.provider"].create(
            {
                "service": "bcv",
                "company_id": cls.company.id,
                "currency_ids": [(6, 0, [cls.usd.id, cls.eur.id])],
            }
        )
        cls.env["res.currency.rate"].search(
            [("company_id", "=", cls.company.id)]
        ).unlink()

    @classmethod
    def _request_handler(cls, s, r, /, **kw):
        if "bcv.org.ve" in (r.url or ""):
            if cls.bcv_raise:
                raise cls.bcv_raise
            response = requests.Response()
            response.status_code = cls.bcv_status_code
            response._content = cls.bcv_content
            return response
        return super()._request_handler(s, r, **kw)

    def _reset_bcv_mock(self):
        type(self).bcv_status_code = 200
        type(self).bcv_content = BCV_HTML
        type(self).bcv_raise = None

    def test_supported_currencies(self):
        currencies = self.provider._get_supported_currencies()
        self.assertEqual(set(currencies), {"EUR", "CNY", "TRY", "RUB", "USD"})

    def test_non_bcv_delegates_to_super(self):
        other = self.env["res.currency.rate.provider"].create(
            {
                "service": "none",
                "company_id": self.company.id,
                "currency_ids": [(6, 0, [self.usd.id])],
            }
        )
        self.assertEqual(other._get_supported_currencies(), [])
        self.assertEqual(
            other._obtain_rates(
                "VES", ["USD"], fields.Date.today(), fields.Date.today()
            ),
            {},
        )

    def test_obtain_rates_uses_iso_date_keys(self):
        today = datetime.now(CARACAS_TZ).date()
        content = self.provider._obtain_rates("VES", ["USD", "EUR"], today, today)
        self.assertEqual(list(content.keys()), [today.isoformat()])
        self.assertAlmostEqual(content[today.isoformat()]["USD"], 1.0 / 36.50)
        self.assertAlmostEqual(content[today.isoformat()]["EUR"], 1.0 / 40.00)

    def test_update_creates_rates(self):
        today = datetime.now(CARACAS_TZ).date()
        self.provider._update(today, today)
        usd_rate = self.env["res.currency.rate"].search(
            [
                ("company_id", "=", self.company.id),
                ("currency_id", "=", self.usd.id),
                ("name", "=", today),
            ]
        )
        self.assertEqual(len(usd_rate), 1)
        self.assertAlmostEqual(usd_rate.rate, 1.0 / 36.50)
        self.assertEqual(usd_rate.provider_id, self.provider)

    @mute_logger(
        "odoo.addons.currency_rate_update_bcv.models.res_currency_rate_provider"
    )
    def test_http_error_returns_empty(self):
        type(self).bcv_status_code = 500
        self.addCleanup(self._reset_bcv_mock)
        today = fields.Date.today()
        content = self.provider._obtain_rates("VES", ["USD"], today, today)
        self.assertEqual(content, {})

    @mute_logger(
        "odoo.addons.currency_rate_update_bcv.models.res_currency_rate_provider"
    )
    def test_network_error_returns_empty(self):
        type(self).bcv_raise = requests.exceptions.Timeout("timeout")
        self.addCleanup(self._reset_bcv_mock)
        today = fields.Date.today()
        content = self.provider._obtain_rates("VES", ["USD"], today, today)
        self.assertEqual(content, {})

    @mute_logger(
        "odoo.addons.currency_rate_update_bcv.models.res_currency_rate_provider"
    )
    def test_unknown_currency_is_skipped(self):
        today = fields.Date.today()
        content = self.provider._obtain_rates("VES", ["GBP"], today, today)
        self.assertEqual(content, {})
