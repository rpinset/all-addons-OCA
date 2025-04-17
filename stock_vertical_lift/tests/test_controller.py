# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import unittest
from unittest import mock

from odoo.tests.common import HttpCase
from odoo.tools import mute_logger

CTRL_PATH = "odoo.addons.stock_vertical_lift.controllers.main.VerticalLiftController"


@unittest.skipIf(os.getenv("SKIP_HTTP_CASE"), "HttpCase skipped")
class TestController(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.shuttle = cls.env.ref(
            "stock_vertical_lift.stock_vertical_lift_demo_shuttle_1"
        )

    @mute_logger("werkzeug")
    def test_fail_if_secret_not_set(self):
        with mock.patch(CTRL_PATH + "._get_env_secret") as mocked:
            mocked.side_effect = Exception("Vertical Lift secret not set")
            data = {"answer": "got it!", "secret": "any"}
            with self.assertLogs(level="ERROR") as log_catcher:
                response = self.url_open("/vertical-lift", data=data)
                self.assertEqual(response.status_code, 500)
                self.assertIn("Vertical Lift secret not set", log_catcher.output[0])

    @mute_logger("werkzeug")
    def test_fail_if_secret_wrong(self):
        with mock.patch(CTRL_PATH + "._get_env_secret") as mocked:
            mocked.return_value = "SECRET"
            data = {"answer": "got it!", "secret": "wrong"}
            with self.assertLogs(level="ERROR") as log_catcher:
                response = self.url_open("/vertical-lift", data=data)
                self.assertEqual(response.status_code, 401)
                logger = "odoo.addons.stock_vertical_lift.controllers.main:secret"
                self.assertEqual(
                    log_catcher.output[0], f"ERROR:{logger} mismatch: 'wrong'"
                )

    def test_record_answer(self):
        self.shuttle.command_ids.create(
            {
                "shuttle_id": self.shuttle.id,
                "command": "0|test|1",
            }
        )
        with mock.patch(CTRL_PATH + "._get_env_secret") as mocked:
            mocked.return_value = "SECRET"
            data = {"answer": "0|test|2", "secret": "SECRET"}
            response = self.url_open("/vertical-lift", data=data)
            self.assertEqual(response.status_code, 200)
            self.shuttle.command_ids.invalidate_recordset()
            self.assertEqual(self.shuttle.command_ids[0].answer, data["answer"])
