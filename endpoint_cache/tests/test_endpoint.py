# Copyright 2024 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import json
import textwrap

from freezegun import freeze_time

from odoo import exceptions

from odoo.addons.endpoint.tests.common import CommonEndpoint
from odoo.addons.website.tools import MockRequest


class TestEndpoint(CommonEndpoint):
    @classmethod
    def _setup_records(cls):
        # pylint: disable=missing-return
        super()._setup_records()
        cls.endpoint1 = cls.env.ref("endpoint.endpoint_demo_1")
        cls.endpoint2 = cls.env.ref("endpoint.endpoint_demo_2")

    def test_cache_name(self):
        self.assertEqual(
            self.endpoint1._endpoint_cache_make_name("json"),
            "endpoint_cache.demo_endpoint_1.json",
        )
        self.assertEqual(
            self.endpoint2._endpoint_cache_make_name("json"),
            "endpoint_cache.demo_endpoint_2.json",
        )

    def test_cache_store_bad_name(self):
        with self.assertRaisesRegex(
            exceptions.UserError, "Cache name must start with 'endpoint_cache'"
        ):
            self.endpoint1._endpoint_cache_store("test", b"test")

    def test_cache_store_and_get(self):
        self.endpoint1._endpoint_cache_store("endpoint_cache.test", b"test")
        data = self.endpoint1._endpoint_cache_get("endpoint_cache.test")
        self.assertEqual(data, b"test")

    def test_cache_gc(self):
        dt1 = "2024-07-01 00:00:00"
        with freeze_time(dt1):
            cache1 = self.endpoint1._endpoint_cache_store(
                "endpoint_cache.test", b"test"
            )
            cache1._write(
                {
                    "create_date": dt1,
                }
            )
        dt2 = "2024-07-10 00:00:00"
        with freeze_time(dt2):
            cache2 = self.endpoint1._endpoint_cache_store(
                "endpoint_cache.test2", b"test2"
            )
            cache2._write(
                {
                    "create_date": dt2,
                }
            )
        dt3 = "2024-07-20 00:00:00"
        with freeze_time(dt3):
            cache3 = self.endpoint1._endpoint_cache_store(
                "endpoint_cache.test3", b"test3"
            )
            cache3._write(
                {
                    "create_date": dt3,
                }
            )
        # 30 days after the 1st cache
        with freeze_time("2024-08-01 00:00:00"):
            self.endpoint1._endpoint_cache_gc()
            self.assertTrue(cache1.exists())
            self.assertTrue(cache2.exists())
            self.assertTrue(cache3.exists())
        # 32 days after the 1st cache
        with freeze_time("2024-08-02 00:00:00"):
            self.endpoint1._endpoint_cache_gc()
            self.assertFalse(cache1.exists())
            self.assertTrue(cache2.exists())
            self.assertTrue(cache3.exists())
        # 32 days after the 2nd cache
        with freeze_time("2024-08-11 00:00:00"):
            self.endpoint1._endpoint_cache_gc()
            self.assertFalse(cache1.exists())
            self.assertFalse(cache2.exists())
            self.assertTrue(cache3.exists())

    def test_action_view_cache_attachments(self):
        action = self.endpoint1.action_view_cache_attachments()
        self.assertEqual(
            action["domain"],
            [
                ("name", "like", "endpoint_cache%"),
                ("res_model", "=", "endpoint.endpoint"),
                ("res_id", "=", self.endpoint1.id),
            ],
        )

    def test_action_purge_cache_attachments(self):
        self.endpoint1._endpoint_cache_store("endpoint_cache.test", b"test")
        self.endpoint1._endpoint_cache_store("endpoint_cache.test2", b"test2")
        self.endpoint2._endpoint_cache_store("endpoint_cache.test3", b"test3")
        self.endpoint1.action_purge_cache_attachments()
        self.assertFalse(self.endpoint1._endpoint_cache_get("endpoint_cache.test"))
        self.assertFalse(self.endpoint1._endpoint_cache_get("endpoint_cache.test2"))
        self.assertTrue(self.endpoint2._endpoint_cache_get("endpoint_cache.test3"))

    def test_action_preheat_cache(self):
        self.endpoint1.code_snippet = textwrap.dedent(
            """
            cache_name = endpoint._endpoint_cache_make_name("json")
            cached = endpoint._endpoint_cache_get(cache_name)
            if cached:
                result = cached
            else:
                result = json.dumps({"foo": "bar"})
                endpoint._endpoint_cache_store(cache_name, result)
            resp = Response(result, content_type="application/json", status=200)
            result = dict(response=resp)
            """
        )
        self.assertEqual(self.endpoint1.cache_att_count, 0)
        with MockRequest(self.env):
            self.endpoint1.action_preheat_cache()
        self.endpoint1.invalidate_recordset(["cache_att_count"])
        self.assertEqual(self.endpoint1.cache_att_count, 1)
        domain = self.endpoint1._endpoint_view_cache_domain()
        cache_atts = self.env["ir.attachment"].search(domain)
        self.assertEqual(cache_atts.mimetype, "application/json")
        self.assertEqual(
            json.loads(base64.decodebytes(cache_atts.datas)), {"foo": "bar"}
        )
