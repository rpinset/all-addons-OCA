# Copyright 2018 Ventor, Xpansa Group <https://ventor.tech/>
# Copyright 2026 Aliaksandr Zubik <alexzub@tut.by> (https://artcloud.by)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
import logging
from collections import defaultdict
from urllib.request import urlopen

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class ResCurrencyRateProviderNBRB(models.Model):
    """Currency rate provider for National Bank of the Republic of Belarus."""

    _inherit = "res.currency.rate.provider"

    service = fields.Selection(
        selection_add=[("NBRB", "National Bank of Belarus (NBRB)")],
        ondelete={"NBRB": "set default"},
    )

    def _get_supported_currencies(self):
        """Return list of currencies supported by NBRB."""
        self.ensure_one()
        if self.service != "NBRB":
            return super()._get_supported_currencies()  # pragma: no cover

        # List of currencies supported by NBRB API
        # This list is dynamically obtained from the API, but we provide
        # a static list for initial setup
        return [
            "AUD",
            "BGN",
            "UAH",
            "DKK",
            "USD",
            "EUR",
            "PLN",
            "IRR",
            "ISK",
            "JPY",
            "CAD",
            "CNY",
            "KWD",
            "MDL",
            "NZD",
            "NOK",
            "RUB",
            "XDR",
            "SGD",
            "KGS",
            "KZT",
            "TRY",
            "GBP",
            "CZK",
            "SEK",
            "CHF",
            "BYN",
        ]

    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        """Download currency rates from NBRB API.

        Args:
            base_currency (str): Base currency code (e.g., 'BYN')
            currencies (list): List of currency codes to fetch
            date_from (date): Start date for rates
            date_to (date): End date for rates

        Returns:
            dict: Dictionary with dates as keys and currency rates as values
                  Format: {'2026-02-13': {'USD': '3.25', 'EUR': '3.52', ...}}
        """
        self.ensure_one()
        if self.service != "NBRB":
            return super()._obtain_rates(
                base_currency, currencies, date_from, date_to
            )  # pragma: no cover

        # NBRB API URL (updated to HTTPS)
        # API documentation: https://www.nbrb.by/apihelp/exrates
        url = "https://www.nbrb.by/API/ExRates/Rates?Periodicity=0"

        _logger.debug("NBRB: Connecting to %s", url)

        try:
            with urlopen(url, timeout=10) as response:
                content = response.read().decode("utf-8")
        except Exception as e:
            raise UserError(_("Error connecting to NBRB API: %s") % str(e)) from e

        try:
            json_data = json.loads(content)
            if not isinstance(json_data, list) or not json_data:
                raise ValueError("Invalid JSON format from NBRB")
        except (json.JSONDecodeError, ValueError) as e:
            raise UserError(
                _("Exchange data format error from National Bank of Belarus: %s")
                % str(e)
            ) from e

        # Extract rate date from first element
        try:
            rate_date_str = json_data[0]["Date"]
            rate_date = fields.Date.from_string(rate_date_str.split("T")[0])
        except (KeyError, IndexError, ValueError) as e:
            raise UserError(
                _("Could not parse rate date from NBRB response: %s") % str(e)
            ) from e

        _logger.debug("NBRB: Rate date is %s", rate_date)

        # Build currency mapping from JSON
        currency_map = {}
        for item in json_data:
            cur_code = item.get("Cur_Abbreviation")
            if cur_code:
                currency_map[cur_code] = {
                    "rate": float(item["Cur_OfficialRate"]),
                    "scale": int(item["Cur_Scale"]),
                }

        # Add BYN to currency map (always 1.0)
        currency_map["BYN"] = {"rate": 1.0, "scale": 1}

        _logger.debug("NBRB: Found %d currencies", len(currency_map))

        # Check if we need to invert calculation
        invert_calculation = False
        if base_currency != "BYN":
            invert_calculation = True
            if base_currency not in currencies:
                currencies.append(base_currency)

        # Calculate rates
        content = defaultdict(dict)
        rate_date_iso = rate_date.isoformat()

        for currency in currencies:
            if currency not in currency_map:
                _logger.warning("NBRB: Currency %s not found in NBRB data", currency)
                continue

            if invert_calculation:
                # Calculate rate relative to base currency (not BYN)
                if base_currency not in currency_map:
                    _logger.error("NBRB: Base currency %s not found", base_currency)
                    continue

                base_rate = (
                    currency_map[base_currency]["rate"]
                    / currency_map[base_currency]["scale"]
                )
                curr_rate = (
                    currency_map[currency]["rate"] / currency_map[currency]["scale"]
                )

                if currency == "BYN":
                    # BYN to base currency
                    rate = base_rate
                else:
                    # Currency to base currency
                    rate = curr_rate / base_rate

            else:
                # BYN is base currency
                if currency == "BYN":
                    rate = 1.0
                else:
                    rate = 1.0 / (
                        currency_map[currency]["rate"] / currency_map[currency]["scale"]
                    )

            content[rate_date_iso][currency] = str(rate)
            _logger.debug("NBRB: 1 %s = %s %s", base_currency, rate, currency)

        return content
