# Copyright (C) 2026 Gray Matter Logic (<https://www.graymatterlogic.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestResConfigSettings(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.ICP = cls.env["ir.config_parameter"].sudo()
        cls.Settings = cls.env["res.config.settings"]

    def test_get_region_selection(self):
        selection = self.Settings.get_region_selection()
        self.assertTrue(selection)
        self.assertTrue(all(len(item) == 2 for item in selection))

    def test_set_and_get_values(self):
        country = self.env["res.country"].search([("code", "=", "US")], limit=1)
        self.assertTrue(country)
        settings = self.Settings.create(
            {
                "google_maps_view_api_key": "test-api-key",
                "google_maps_lang_localization": "en",
                "google_maps_region_localization": country.code,
                "google_maps_theme": "night",
                "google_maps_places": True,
                "google_maps_geometry": True,
            }
        )
        settings.set_values()
        self.assertEqual(self.ICP.get_param("google.api_key_geocode"), "test-api-key")
        self.assertEqual(self.ICP.get_param("google.lang_localization"), "&language=en")
        self.assertEqual(self.ICP.get_param("google.region_localization"), "&region=US")
        self.assertEqual(self.ICP.get_param("google.maps_theme"), "night")
        self.assertEqual(self.ICP.get_param("google.maps_libraries"), "geometry,places")
        values = self.Settings.get_values()
        self.assertEqual(values["google_maps_view_api_key"], "test-api-key")
        self.assertEqual(values["google_maps_lang_localization"], "en")
        self.assertEqual(values["google_maps_region_localization"], "US")
        self.assertEqual(values["google_maps_theme"], "night")
        self.assertTrue(values["google_maps_places"])
        self.assertTrue(values["google_maps_geometry"])

    def test_set_values_without_localization_and_libraries(self):
        settings = self.Settings.create(
            {
                "google_maps_view_api_key": "key-2",
                "google_maps_lang_localization": False,
                "google_maps_region_localization": False,
                "google_maps_theme": "default",
                "google_maps_places": False,
                "google_maps_geometry": False,
            }
        )
        settings.set_values()
        self.assertFalse(self.ICP.get_param("google.lang_localization"))
        self.assertFalse(self.ICP.get_param("google.region_localization"))
        self.assertEqual(self.ICP.get_param("google.maps_libraries"), ",")
        values = self.Settings.get_values()
        self.assertFalse(values["google_maps_lang_localization"])
        self.assertFalse(values["google_maps_region_localization"])
        self.assertFalse(values["google_maps_places"])
        self.assertFalse(values["google_maps_geometry"])

    def test_onchange_lang_localization_clears_region(self):
        country = self.env["res.country"].search([("code", "=", "FR")], limit=1)
        settings = self.Settings.new(
            {
                "google_maps_lang_localization": "fr",
                "google_maps_region_localization": country.code,
            }
        )
        settings.google_maps_lang_localization = False
        settings.onchange_lang_localization()
        self.assertFalse(settings.google_maps_region_localization)

    def test_helper_methods_direct(self):
        settings = self.Settings.create(
            {
                "google_maps_lang_localization": "it",
                "google_maps_region_localization": "IT",
                "google_maps_places": True,
                "google_maps_geometry": False,
            }
        )
        self.assertEqual(settings._set_google_maps_lang_localization(), "&language=it")
        self.assertEqual(settings._set_google_maps_region_localization(), "&region=IT")
        self.assertEqual(settings._set_google_maps_places(), "places")
        self.assertEqual(settings._set_google_maps_geometry(), "")
        self.ICP.set_param("google.lang_localization", "")
        self.ICP.set_param("google.region_localization", "")
        self.ICP.set_param("google.maps_libraries", "")
        self.assertEqual(self.Settings._get_google_maps_lang_localization(), "")
        self.assertEqual(self.Settings._get_google_maps_region_localization(), "")
        self.assertFalse(self.Settings._get_google_maps_places())
        self.assertFalse(self.Settings._get_google_maps_geometry())
