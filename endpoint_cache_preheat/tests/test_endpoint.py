# Copyright 2025 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import textwrap
from datetime import datetime

from dateutil.relativedelta import relativedelta
from freezegun import freeze_time

from odoo import fields

from odoo.addons.endpoint.tests.common import CommonEndpoint
from odoo.addons.queue_job.tests.common import trap_jobs
from odoo.addons.website.tools import MockRequest


class TestEndpoint(CommonEndpoint):
    @classmethod
    def _setup_records(cls):
        # pylint: disable=missing-return
        super()._setup_records()
        cls.endpoint1 = cls.env.ref("endpoint.endpoint_demo_1")
        cls.cron = cls.env.ref("endpoint_cache_preheat.cron_endpoint_cache_preheat")

    def _run_cron(self):
        with MockRequest(self.env):
            self.cron.ir_actions_server_id.run()

    def test_cron_preheat_cache(self):
        self.assertFalse(self.endpoint1.cache_preheat)
        self.assertFalse(self.endpoint1.cache_preheat_ts)
        now = datetime.now().replace(microsecond=0)
        ep_daily = self.endpoint1.copy({"route": "/daily"})
        ep_daily.cache_preheat = True
        ep_daily.cache_preheat_ts = now
        ep_daily.code_snippet = textwrap.dedent(
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
        ep_weekly = ep_daily.copy({"route": "/weekly", "cache_policy": "week"})
        ep_monthly = ep_daily.copy({"route": "/monthly", "cache_policy": "month"})

        # 1 day later
        future_date_1 = now + relativedelta(days=1)
        with trap_jobs() as trap, freeze_time(future_date_1), MockRequest(self.env):
            self._run_cron()
            trap.assert_jobs_count(1)
            trap.assert_enqueued_job(ep_daily._cron_endpoint_cache_preheat)
            trap.perform_enqueued_jobs()
            self.assertEqual(ep_daily.cache_preheat_ts, future_date_1)
            self.assertEqual(ep_weekly.cache_preheat_ts, now)
            self.assertEqual(ep_monthly.cache_preheat_ts, now)

        self.assertEqual(
            self.env["ir.attachment"].search_count(
                ep_daily._endpoint_view_cache_domain()
            ),
            1,
        )
        self.assertEqual(
            self.env["ir.attachment"].search_count(
                ep_weekly._endpoint_view_cache_domain()
            ),
            0,
        )
        self.assertEqual(
            self.env["ir.attachment"].search_count(
                ep_monthly._endpoint_view_cache_domain()
            ),
            0,
        )

        # 2 days later
        future_date_2 = now + relativedelta(days=2)
        with trap_jobs() as trap, freeze_time(future_date_2), MockRequest(self.env):
            self._run_cron()
            trap.assert_jobs_count(1)
            trap.assert_enqueued_job(ep_daily._cron_endpoint_cache_preheat)
            trap.perform_enqueued_jobs()
            self.assertEqual(ep_daily.cache_preheat_ts, future_date_2)
            self.assertEqual(ep_weekly.cache_preheat_ts, now)
            self.assertEqual(ep_monthly.cache_preheat_ts, now)

        self.assertEqual(
            self.env["ir.attachment"].search_count(
                ep_daily._endpoint_view_cache_domain()
            ),
            2,
        )
        self.assertEqual(
            self.env["ir.attachment"].search_count(
                ep_weekly._endpoint_view_cache_domain()
            ),
            0,
        )
        self.assertEqual(
            self.env["ir.attachment"].search_count(
                ep_monthly._endpoint_view_cache_domain()
            ),
            0,
        )

        # 1 week later
        future_date_3 = now + relativedelta(weeks=1)
        with trap_jobs() as trap, freeze_time(future_date_3), MockRequest(self.env):
            self._run_cron()
            trap.assert_jobs_count(2)
            trap.assert_enqueued_job(ep_daily._cron_endpoint_cache_preheat)
            trap.perform_enqueued_jobs()
            self.assertEqual(ep_daily.cache_preheat_ts, future_date_3)
            self.assertEqual(ep_weekly.cache_preheat_ts, future_date_3)
            self.assertEqual(ep_monthly.cache_preheat_ts, now)

        self.assertEqual(
            self.env["ir.attachment"].search_count(
                ep_daily._endpoint_view_cache_domain()
            ),
            3,
        )
        self.assertEqual(
            self.env["ir.attachment"].search_count(
                ep_weekly._endpoint_view_cache_domain()
            ),
            1,
        )
        self.assertEqual(
            self.env["ir.attachment"].search_count(
                ep_monthly._endpoint_view_cache_domain()
            ),
            0,
        )

        # 1 month later
        future_date_4 = now + relativedelta(months=1)
        with trap_jobs() as trap, freeze_time(future_date_4), MockRequest(self.env):
            self._run_cron()
            trap.assert_jobs_count(3)
            trap.assert_enqueued_job(ep_daily._cron_endpoint_cache_preheat)
            trap.perform_enqueued_jobs()
            self.assertEqual(ep_daily.cache_preheat_ts, future_date_4)
            self.assertEqual(ep_weekly.cache_preheat_ts, future_date_4)
            self.assertEqual(ep_monthly.cache_preheat_ts, future_date_4)

        self.assertEqual(
            self.env["ir.attachment"].search_count(
                ep_daily._endpoint_view_cache_domain()
            ),
            4,
        )
        self.assertEqual(
            self.env["ir.attachment"].search_count(
                ep_weekly._endpoint_view_cache_domain()
            ),
            2,
        )
        self.assertEqual(
            self.env["ir.attachment"].search_count(
                ep_monthly._endpoint_view_cache_domain()
            ),
            1,
        )

    def test_cron_preheat_cache_disabled(self):
        now = fields.Datetime.from_string("2025-02-19 23:00:00")
        ep_daily = self.endpoint1.copy({"route": "/daily"})
        ep_daily.cache_preheat = False
        ep_daily.cache_preheat_ts = now
        ep_daily.code_snippet = textwrap.dedent(
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
        # 1 day later
        future_date = fields.Datetime.from_string("2025-02-20 20:00:00")
        with trap_jobs() as trap, freeze_time(future_date), MockRequest(self.env):
            self._run_cron()
            trap.assert_jobs_count(0)
            self.assertEqual(ep_daily.cache_preheat_ts, now)

    def test_action_preheat_cache_async(self):
        ep_daily = self.endpoint1.copy({"route": "/daily"})
        ep_daily.cache_preheat = True
        ep_daily.code_snippet = textwrap.dedent(
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
        now = fields.Datetime.from_string("2025-02-19 23:00:00")
        with trap_jobs() as trap, freeze_time(now), MockRequest(self.env):
            ep_daily.action_preheat_cache_async()
            trap.assert_jobs_count(1)
            trap.assert_enqueued_job(ep_daily._cron_endpoint_cache_preheat)
            trap.perform_enqueued_jobs()
        self.assertEqual(ep_daily.cache_preheat_ts, now)

    def test_action_cache_purge(self):
        # purging cache should reset the TS
        self.endpoint1.cache_preheat_ts = fields.Datetime.now()
        self.endpoint1.action_purge_cache_attachments()
        self.assertFalse(self.endpoint1.cache_preheat_ts)
