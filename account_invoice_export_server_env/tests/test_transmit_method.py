# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import os
from unittest.mock import patch

from odoo.tools.config import config as odoo_config

from odoo.addons.server_environment.tests.common import ServerEnvironmentCase


class TestTransmitMethodServerEnv(ServerEnvironmentCase):
    @patch.dict(odoo_config.options, {"running_env": "test"})
    def test_server_env_fields_are_loaded(self):
        """Create the transmit.method record with a code matching the conf section"""
        config_dir = os.path.join(os.path.dirname(__file__), "testfiles")
        with self.load_config(config_dir=config_dir):
            defaults = self.env["transmit.method"].default_get(
                [
                    "code",
                    "name",
                    "destination_user",
                    "destination_pwd",
                    "destination_url",
                ]
            )
            defaults.update(
                {"code": "transmition_method_code", "name": "Test Transmit Method"}
            )
            test_transmit_method = self.env["transmit.method"].create(defaults)
            self.assertEqual(test_transmit_method.destination_user, "test_user")
            self.assertEqual(test_transmit_method.destination_pwd, "test_password")
            self.assertEqual(
                test_transmit_method.destination_url, "https://api.example.com"
            )
