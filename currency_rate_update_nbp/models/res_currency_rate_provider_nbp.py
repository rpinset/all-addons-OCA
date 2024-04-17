# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import requests
from lxml import etree

from odoo import fields, models


class ResCurrencyRateProviderNBP(models.Model):
    _inherit = "res.currency.rate.provider"

    service = fields.Selection(
        selection_add=[("NBP", "National Bank of Poland")],
        ondelete={"NBP": "set default"},
    )

    def rate_retrieve(self, dom, ns, curr):
        """Parse a dom node to retrieve currencies data"""
        res = {}
        xpath_rate_currency = (
            "/tabela_kursow/pozycja[kod_waluty='%s']/" "kurs_sredni/text()"
        ) % (curr.upper())
        xpath_rate_ref = (
            "/tabela_kursow/pozycja[kod_waluty='%s']/" "przelicznik/text()"
        ) % (curr.upper())
        res["rate_currency"] = float(
            dom.xpath(xpath_rate_currency, namespaces=ns)[0].replace(",", ".")
        )
        res["rate_ref"] = float(dom.xpath(xpath_rate_ref, namespaces=ns)[0])
        return res

    def _get_supported_currencies(self):
        """Return list of currencies supported by NBP"""
        self.ensure_one()
        if self.service != "NBP":
            return super()._get_supported_currencies()  # pragma: no cover

        # List of currencies obrained from:
        # https://www.nbp.pl/kursy/xml/LastA.xml + PLN
        return [
            "THB",
            "USD",
            "AUD",
            "HKD",
            "CAD",
            "NZD",
            "SGD",
            "EUR",
            "HUF",
            "CHF",
            "GBP",
            "UAH",
            "JPY",
            "CZK",
            "DKK",
            "ISK",
            "NOK",
            "SEK",
            "HRK",
            "RON",
            "BGN",
            "TRY",
            "ILS",
            "CLP",
            "PHP",
            "MXN",
            "ZAR",
            "BRL",
            "MYR",
            "RUB",
            "IDR",
            "INR",
            "KRW",
            "CNY",
            "XDR",
            "PLN",
        ]

    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        """Make request to NBP and fetch today's rates"""
        self.ensure_one()
        if self.service != "NBP":
            return super()._obtain_rates(
                base_currency, currencies, date_from, date_to
            )  # pragma: no cover

        # LastA.xml is always the most recent one
        url = "https://static.nbp.pl/dane/kursy/xml/LastA.xml"
        content = requests.get(url, timeout=5).content

        dom = etree.fromstring(content)
        ns = {}
        rate_date = dom.xpath("/tabela_kursow/data_publikacji/text()", namespaces=ns)[0]
        res = {rate_date: {}}

        main_rate = 1.0
        if base_currency != "PLN":
            main_curr_data = self.rate_retrieve(dom, ns, base_currency)
            main_rate = main_curr_data["rate_currency"] / main_curr_data["rate_ref"]

        for curr in currencies:
            if curr == "PLN":
                rate = main_rate
            else:
                curr_data = self.rate_retrieve(dom, ns, curr)
                rate = main_rate * curr_data["rate_ref"] / curr_data["rate_currency"]
            res[rate_date][curr] = rate

        return res
