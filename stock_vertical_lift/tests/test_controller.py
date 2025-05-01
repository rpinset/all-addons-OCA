# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import unittest
from unittest import mock

from odoo.tests.common import HttpCase
from odoo.tools import mute_logger


@unittest.skipIf(os.getenv("SKIP_HTTP_CASE"), "HttpCase skipped")
class TestController(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.shuttle = cls.env.ref(
            "stock_vertical_lift.stock_vertical_lift_demo_shuttle_1"
        )

    @mute_logger("werkzeug")
    def test_fail_if_secret_not_passed(self):
        data = {"answer": "got it!", "secret": ""}
        with self.assertLogs(level="ERROR") as log_catcher:
            response = self.url_open("/vertical-lift", data=data)
            self.assertEqual(response.status_code, 401)
            self.assertIn("Vertical Lift secret not received", log_catcher.output[0])

    @mute_logger("werkzeug")
    def test_fail_if_secret_not_configured(self):
        data = {"answer": "got it!", "secret": "SECRET"}
        with self.assertLogs(level="ERROR") as log_catcher:
            response = self.url_open("/vertical-lift", data=data)
            self.assertEqual(response.status_code, 401)
            self.assertIn("Vertical Lift secret not configured.", log_catcher.output[0])

    @mute_logger("werkzeug")
    def test_fail_if_secret_param_wrong(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "stock_vertical_lift.secret", "SECRET"
        )
        data = {"answer": "got it!", "secret": "wrong"}
        with self.assertLogs(level="ERROR") as log_catcher:
            response = self.url_open("/vertical-lift", data=data)
            self.assertEqual(response.status_code, 401)
            logger = "odoo.addons.stock_vertical_lift.controllers.main:secret"
            self.assertEqual(log_catcher.output[0], f"ERROR:{logger} mismatch: 'wrong'")

    @mute_logger("werkzeug")
    @mock.patch.dict(os.environ, {"VERTICAL_LIFT_SECRET": "SECRET"})
    def test_fail_if_secret_env_wrong(self):
        data = {"answer": "got it!", "secret": "wrong"}
        with self.assertLogs(level="ERROR") as log_catcher:
            response = self.url_open("/vertical-lift", data=data)
            self.assertEqual(response.status_code, 401)
            logger = "odoo.addons.stock_vertical_lift.controllers.main:secret"
            self.assertEqual(log_catcher.output[0], f"ERROR:{logger} mismatch: 'wrong'")

    def _test_record_answer(self):
        self.shuttle.command_ids.create(
            {
                "shuttle_id": self.shuttle.id,
                "command": "0|test|1",
            }
        )
        data = {"answer": "0|test|2", "secret": "SECRET"}
        response = self.url_open("/vertical-lift", data=data)
        self.assertEqual(response.status_code, 200)
        self.shuttle.command_ids.invalidate_recordset()
        self.assertEqual(self.shuttle.command_ids[0].answer, data["answer"])

    @mock.patch.dict(os.environ, {"VERTICAL_LIFT_SECRET": "SECRET"})
    def test_record_answer_with_env_var(self):
        self._test_record_answer()

    def test_record_answer_with_param(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "stock_vertical_lift.secret", "SECRET"
        )
        self._test_record_answer()
