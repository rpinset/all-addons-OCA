# Copyright 2023 DAJ MI 5
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import json
import logging
import urllib.request as request

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResCurrencyRateProviderHrHNB(models.Model):
    _inherit = "res.currency.rate.provider"

    service = fields.Selection(
        selection_add=[("HR-HNB", "Croatia-HNB")],
        ondelete={"HR-HNB": "set default"},
    )

    def _get_supported_currencies(self):
        self.ensure_one()
        if self.service != "HR-HNB":
            return super()._get_supported_currencies()  # pragma: no cover

        data = self._l10n_hr_hnb_urlopen()
        currencies = [c["valuta"] for c in data]
        # BOLE: ovo paziti jer moguce je da bas na taj dan nemam
        # sve valute.. ali very low impact pa se ne mucim oko ovog
        return currencies

    def _get_rate_type(self):
        rate_type = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("currency_rate_update_hr_hnb.rate_type")
        )
        if not type:
            rate_type = "srednji"
        return rate_type + "_tecaj"

    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        self.ensure_one()
        if self.service != "HR-HNB":
            return super()._obtain_rates(
                base_currency, currencies, date_from, date_to
            )  # pragma: no cover
        rate_type = self._get_rate_type()
        result = {}
        currencies = [c.name for c in self.currency_ids]
        data = self._l10n_hr_hnb_urlopen(
            currencies=currencies, date_from=date_from, date_to=date_to
        )
        for cd in data:
            currency = cd["valuta"]
            if currency not in currencies:
                continue
            rate_date = cd["datum_primjene"]
            rate = cd.get(rate_type).replace(",", ".")
            try:
                rate = float(rate)
            except Exception as E:
                _logger.debug("HNB problem rate : ", str(cd), repr(E))
                continue
            if not result.get(rate_date):
                result[rate_date] = {currency: rate}
            else:
                result[rate_date].update({currency: rate})
        return result

    def _l10n_hr_hnb_urlopen(self, currencies=None, date_from=None, date_to=None):
        url = "https://api.hnb.hr/tecajn-eur/v3"
        if date_from is not None:
            if date_to is not None:
                url += "?datum-primjene-od=%s&datum-primjene-do=%s" % (
                    fields.Date.to_string(date_from),
                    fields.Date.to_string(date_to),
                )
        if currencies is not None:
            cur = "&".join(["valuta=" + c for c in currencies])
            url += "?" + cur

        res = request.urlopen(url, timeout=15)
        data = json.loads(res.read().decode("UTF-8"))
        return data
