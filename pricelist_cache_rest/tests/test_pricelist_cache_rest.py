# Copyright 2021 Camptocamp SA (http://www.camptocamp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import contextlib
import json

from freezegun import freeze_time
from werkzeug.exceptions import Unauthorized

from odoo.addons.pricelist_cache.tests.common import (
    LIST_PRICES_MAPPING,
    TestPricelistCacheCommon,
)
from odoo.addons.pricelist_cache_rest.controllers.main import PricelistController
from odoo.addons.website.tools import MockRequest


# Usa a date that's consistent w/ LIST_PRICES_MAPPING: it uses the prices  defined in
# ``pricelist_cache/data/demo.xml``, and some of them have time-limited validity
@freeze_time("2021-03-15")
class TestPricelistCacheRest(TestPricelistCacheCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.api_key = cls.env.ref("pricelist_cache_rest.api_key_demo")
        cls.api_key2 = cls.env.ref("pricelist_cache_rest.api_key_demo_2")
        cls.env.company.pricelist_cache_auhorize_apikey_ids += cls.api_key
        cls.ctrl = PricelistController()

    @contextlib.contextmanager
    def _get_mocked_request(self, httprequest=None, extra_headers=None):
        with MockRequest(self.env) as mocked_request:
            mocked_request.httprequest = httprequest or mocked_request.httprequest
            headers = {}
            headers.update(extra_headers or {})
            mocked_request.httprequest.headers = headers
            mocked_request.auth_api_key_id = self.api_key.id
            mocked_request.make_response = lambda data, **kw: data
            yield mocked_request

    def test_api_key_validation(self):
        with self._get_mocked_request() as req:
            req.auth_api_key_id = None
            with self.assertRaisesRegex(Unauthorized, "API key missing"):
                self.ctrl.partner_pricelist(self.partner)
        with self._get_mocked_request() as req:
            req.auth_api_key_id = self.api_key2.id
            with self.assertRaisesRegex(Unauthorized, "API key not valid"):
                self.ctrl.partner_pricelist(self.partner)

    def _resp_data(self, resp):
        return json.loads(resp.data.decode())

    def test_get_prices(self):
        partner = self.partner
        for pricelist_xmlid, expected_result in LIST_PRICES_MAPPING.items():
            partner.property_product_pricelist = self.env.ref(pricelist_xmlid)
            with self._get_mocked_request():
                resp = self.ctrl.partner_pricelist(partner)
                data = self._resp_data(resp)
                result = list(filter(lambda c: c["id"] in self.products.ids, data))
                result.sort(key=lambda r: r["id"])
                expected_result.sort(key=lambda r: r["id"])
                self.assertEqual(result, expected_result)
