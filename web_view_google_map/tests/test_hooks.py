# Copyright (C) 2026 Gray Matter Logic (<https://www.graymatterlogic.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.web_view_google_map.hooks import uninstall_hook


class TestUninstallHook(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.Action = cls.env["ir.actions.act_window"]

    def test_uninstall_hook_strips_google_map_view_mode(self):
        action_mid = self.Action.create(
            {
                "name": "Partners Mid Google Map",
                "res_model": "res.partner",
                "view_mode": "list,google_map,form",
            }
        )
        action_start = self.Action.create(
            {
                "name": "Partners Start Google Map",
                "res_model": "res.partner",
                "view_mode": "google_map,list,form",
            }
        )
        action_only = self.Action.create(
            {
                "name": "Partners Only Google Map",
                "res_model": "res.partner",
                "view_mode": "google_map",
            }
        )
        uninstall_hook(self.env)
        self.env.invalidate_all()
        self.assertEqual(action_mid.view_mode, "list,form")
        self.assertEqual(action_start.view_mode, "list,form")
        self.assertFalse(action_only.exists())
