# Copyright 2023 Luis Pinzón
# Copyright 2026 Anderson Armeya
# Copyright 2026 andyengit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from lxml import etree

from odoo import fields, models

_logger = logging.getLogger(__name__)

TIMEOUT = (10, 60)
MONEDAS = {"EUR": "euro", "CNY": "yuan", "TRY": "lira", "RUB": "rublo", "USD": "dolar"}
CARACAS_TZ = ZoneInfo("America/Caracas")  # se necesita porque la hora de bcv es de vzla


class ResCurrencyRateProvider(models.Model):
    _inherit = "res.currency.rate.provider"
    service = fields.Selection(
        selection_add=[("bcv", "BCV scrapping")],
        ondelete={"bcv": "set default"},
        default="bcv",
    )

    def _get_supported_currencies(self):
        self.ensure_one()
        if self.service != "bcv":
            return super()._get_supported_currencies()
        return list(MONEDAS.keys())

    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        self.ensure_one()
        if self.service != "bcv":
            return super()._obtain_rates(base_currency, currencies, date_from, date_to)

        content = defaultdict(dict)

        bcv_data = self._scrap(currencies)

        for k, v in bcv_data.items():
            dt = v[1].date().isoformat()
            content[dt][k] = v[0]

        return content

    def _scrap(self, available_currencies):
        request_url = "http://www.bcv.org.ve/"

        rslt = {}
        try:
            fetched_data = requests.get(request_url, verify=False, timeout=TIMEOUT)
        except Exception as e:
            _logger.debug("%s, %s", self._name, e)
            return rslt

        if fetched_data.status_code != 200:
            _logger.debug("%s, HTTP %s", self._name, fetched_data.status_code)
            return rslt

        available_currency_names = available_currencies

        htmlelem = etree.fromstring(fetched_data.content, etree.HTMLParser())

        dt = datetime.now(CARACAS_TZ)
        for currency_name in available_currency_names:
            try:
                if currency_name in ["Bs", "VES", "VEF", "VED"]:
                    rslt[currency_name] = (1.0, dt)
                else:
                    sValue = htmlelem.xpath(
                        f".//div[@id='{MONEDAS[currency_name]}']/div/div/div[2]/strong"
                    )[0].text
                    value = float(sValue.replace(" ", "").replace(",", "."))

                    rslt[currency_name] = (1.0 / value, dt)
            except Exception as e:
                _logger.debug("%s, %s", self._name, e)

        return rslt
