# Copyright (C) 2026 Gray Matter Logic (<https://www.graymatterlogic.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestGoogleMapView(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.View = cls.env["ir.ui.view"]
        cls.ActWindowView = cls.env["ir.actions.act_window.view"]

    def test_view_type_selection(self):
        selection = dict(self.View._fields["type"].selection)
        self.assertIn("google_map", selection)
        self.assertEqual(selection["google_map"], "Google Maps")

    def test_act_window_view_mode_selection(self):
        selection = dict(self.ActWindowView._fields["view_mode"].selection)
        self.assertIn("google_map", selection)
        self.assertEqual(selection["google_map"], "Google Maps")

    def test_get_view_info_contains_google_map(self):
        info = self.View._get_view_info()
        self.assertIn("google_map", info)
        self.assertEqual(info["google_map"]["icon"], "fa fa-map-o")

    def test_partner_google_map_view_exists(self):
        view = self.env.ref("web_view_google_map.view_res_partner_google_map")
        self.assertEqual(view.type, "google_map")
        self.assertEqual(view.model, "res.partner")
        self.assertIn("partner_latitude", view.arch)
        self.assertIn("partner_longitude", view.arch)

    def test_partner_action_includes_google_map(self):
        action = self.env.ref("base.action_partner_form")
        self.assertIn("google_map", action.view_mode)
