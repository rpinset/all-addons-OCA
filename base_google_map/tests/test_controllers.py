# Copyright (C) 2026 Gray Matter Logic (<https://www.graymatterlogic.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.base_google_map.controllers.main import Main


class TestControllers(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.ICP = cls.env["ir.config_parameter"].sudo()
        cls.controller = Main()

    def test_map_theme(self):
        self.ICP.set_param("google.maps_theme", "retro")
        with patch("odoo.addons.base_google_map.controllers.main.http") as mock_http:
            mock_http.request.env = self.env
            result = self.controller.map_theme()
        self.assertEqual(result, {"theme": "retro"})

    def test_google_autocomplete_conf_with_lang(self):
        self.ICP.set_param("web_google_maps.autocomplete_lang_restrict", "True")
        self.ICP.set_param("web_google_maps.lang_localization", "en")
        with patch("odoo.addons.base_google_map.controllers.main.http") as mock_http:
            mock_http.request.env = self.env
            result = self.controller.google_autocomplete_settings()
        self.assertEqual(result, {"language": "en"})

    def test_google_autocomplete_conf_without_restrict(self):
        self.ICP.set_param("web_google_maps.autocomplete_lang_restrict", "False")
        self.ICP.set_param("web_google_maps.lang_localization", "fr")
        with patch("odoo.addons.base_google_map.controllers.main.http") as mock_http:
            mock_http.request.env = self.env
            result = self.controller.google_autocomplete_settings()
        self.assertEqual(result, {})

    def test_google_autocomplete_conf_restrict_without_lang(self):
        self.ICP.set_param("web_google_maps.autocomplete_lang_restrict", "True")
        self.ICP.set_param("web_google_maps.lang_localization", False)
        with patch("odoo.addons.base_google_map.controllers.main.http") as mock_http:
            mock_http.request.env = self.env
            result = self.controller.google_autocomplete_settings()
        self.assertEqual(result, {})
