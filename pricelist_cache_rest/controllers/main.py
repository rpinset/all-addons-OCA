# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import json
from typing import Any

from werkzeug.exceptions import Unauthorized

from odoo import api, http, models


class PricelistController(http.Controller):
    """Expose prices for pricelists."""

    @http.route(
        "/pricelist/<model('res.partner'):partner>",
        type="http",
        auth="api_key",
        methods=["GET"],
        csrf=False,
    )
    def partner_pricelist(self, partner: models.Model) -> http.Response:
        """Retrieves all prices for the given partner"""
        req = http.request
        self._validate_api_key(req.env, getattr(req, "auth_api_key_id", None))
        cache_items = self._get_cache_items(partner)
        json_data = self._cache_to_json(cache_items)
        return self._make_json_response(json_data)

    def _validate_api_key(self, env: api.Environment, api_key_id: int = None) -> None:
        """Validates the given API key

        A ``werkzeug.exceptions.Unauthorized`` error is raised for missing/invalid keys.
        """
        if api_key_id is None:
            raise Unauthorized("API key missing")
        elif api_key_id not in self._get_authorized_api_keys(env):
            raise Unauthorized("API key not valid")

    def _get_authorized_api_keys(self, env: api.Environment) -> list[int]:
        """Retrieves pricelists' authorized API Keys from the env's company"""
        # TODO: what about multi company support?
        return env.company.pricelist_cache_auhorize_apikey_ids.ids

    def _get_cache_items(self, partner: models.Model) -> models.Model:
        """Retrieves ``product.pricelist.cache`` records from the current partner"""
        return partner._pricelist_cache_get_prices()

    def _cache_to_json(self, cache_items: models.Model) -> list[Any]:
        exporter = cache_items.env.ref("pricelist_cache_rest.ir_exp_cache_item")
        return cache_items.jsonify(exporter.get_json_parser())

    def _make_json_response(self, data: list[Any]) -> http.Response:
        headers = {"Content-Type": "application/json"}
        return http.request.make_response(json.dumps(data), headers=headers)
