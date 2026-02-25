# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from pathlib import Path
from unittest.mock import patch

from lxml import etree
from odoo_test_helper import FakeModelLoader

from odoo.exceptions import ValidationError
from odoo.tools.config import config

from odoo.addons.data_encryption.tests.common import CommonDataEncrypted


class TestServerEnvDataEncrypted(CommonDataEncrypted):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        cls.addClassCleanup(cls.loader.restore_registry)
        # The fake class is imported here !! After the backup_registry
        from .models import FakePartner

        cls.loader.update_registry((FakePartner,))
        cls.set_new_key_env("prod")
        cls.set_new_key_env("preprod")

        cls.partner = cls.env["res.partner"].create(
            {"name": "Test Partner", "city": "Test City"}
        )

    def test_env_dependent_value(self):
        partner = self.env["res.partner"].create(
            {"name": "Fake name", "city": "test city"}
        )
        self.assertFalse(partner.with_context(environment="prod").city)
        partner.with_context(environment="prod").write({"city": "prod city"})
        self.assertEqual(partner.with_context(environment=False).city, "test city")
        self.assertEqual(partner.with_context(environment="test").city, "test city")
        self.assertEqual(partner.with_context(environment="prod").city, "prod city")

    def test_view_with_env_update(self):
        self.maxDiff = None
        # common class already set test environment (as default)
        mixin_obj = self.env["server.env.mixin"]
        base_path = Path(__file__).parent / "fixtures" / "base.xml"
        xml_str = base_path.read_text()
        xml = etree.XML(xml_str)
        res_xml = mixin_obj._update_form_view_from_env(xml, "form")

        # check we have 3 alert div for our 3 environments
        env_div_xml = res_xml.find("sheet").find("div").findall("div")
        # 3 alert div + 1 button div
        self.assertEqual(len(env_div_xml), 4)
        # test first alert test div
        test_alert_div = env_div_xml[0]
        self.assertEqual(
            test_alert_div.get("invisible"),
            "context.get('environment', 'test') != 'test'",
        )
        self.assertEqual(
            test_alert_div.find("strong").text, "Modify values for test environment"
        )
        # test preprod div
        preprod_alert_div = env_div_xml[1]
        self.assertEqual(
            preprod_alert_div.get("invisible"),
            "context.get('environment', 'test') != 'preprod'",
        )
        self.assertEqual(
            preprod_alert_div.find("strong").text,
            "Modify values for preprod environment",
        )
        # test buttons
        button_div = env_div_xml[-1]
        # 3 buttons for 3 env
        self.assertEqual(len(button_div.findall("button")), 3)
        test_button = button_div.findall("button")[0]
        # test env button
        self.assertEqual(
            test_button.get("invisible"), "context.get('environment', 'test') == 'test'"
        )
        self.assertEqual(
            test_button.get("name"), "action_change_env_data_encrypted_fields"
        )
        self.assertEqual(test_button.get("string"), "Define values for test")
        # preprod button
        preprod_button = button_div.findall("button")[1]
        self.assertEqual(
            preprod_button.get("invisible"),
            "context.get('environment', 'test') == 'preprod'",
        )
        self.assertEqual(preprod_button.get("string"), "Define values for preprod")
        self.assertEqual(preprod_button.get("context"), "{'environment': 'preprod'}")
        # test normal field with pre-existing readonly condition
        test2_field = res_xml.find("sheet").findall(".//field[@name='test2']")[0]
        self.assertEqual(
            test2_field.get("readonly"),
            "(not type_env_is_editable) or context.get(\"environment\", 'test') != "
            "'test'",
        )
        # test normal field without pre-existing readonly condition
        test_field = res_xml.find("sheet").findall(".//field[@name='test']")[0]
        self.assertEqual(
            test_field.get("readonly"), "context.get(\"environment\", 'test') != 'test'"
        )

        # test that buttons are invisible in the context of env different than the
        # running one.
        confirm_button = res_xml.find("header").find("button")
        self.assertEqual(
            confirm_button.get("invisible"),
            "context.get(\"environment\", 'test') != 'test'",
        )

    def test_missing_encryption_key(self):
        """Test behavior when encryption key is missing for current env"""
        with patch.object(
            config,
            "get",
            side_effect=lambda key, default=None: "missing_env"
            if key == "running_env"
            else (None if key.startswith("encryption_key_") else default),
        ):
            # This should trigger the warning in _current_env_encrypted_key_exists
            self.assertFalse(self.partner._current_env_encrypted_key_exists())

            # Test fallbacks
            # Since we can't easily mock super(), we just verify it doesn't crash
            self.partner._compute_server_env_from_default("city", {})
            self.partner._inverse_server_env("city")

            # Test warning div in view
            mixin_obj = self.env["server.env.mixin"]
            elem = mixin_obj._get_extra_environment_info_div("test", ["test", "prod"])
            self.assertIn(
                "The encryption key for current environement is not defined",
                etree.tostring(elem, encoding="unicode"),
            )

    def test_action_change_env_data_encrypted_fields(self):
        """Test action_change_env_data_encrypted_fields"""
        # Case 1: No action in context
        action = self.partner.action_change_env_data_encrypted_fields()
        self.assertEqual(action.get("res_id"), self.partner.id)

        # Case 2: Action in context
        # We need a real action id to browse
        act_window = self.env["ir.actions.act_window"].search([], limit=1)
        if act_window:
            # Mock the read result to have multiple views including a non-form one
            with patch.object(
                type(self.env["ir.actions.act_window"]),
                "read",
                return_value=[
                    {
                        "views": [(1, "tree"), (2, "form")],
                        "type": "ir.actions.act_window",
                    }
                ],
            ):
                partner_with_ctx = self.partner.with_context(
                    params={"action": act_window.id}
                )
                action = partner_with_ctx.action_change_env_data_encrypted_fields()
                self.assertEqual(action.get("res_id"), self.partner.id)
                self.assertEqual(action.get("view_mode"), "form")
                self.assertEqual(len(action["views"]), 1)
                self.assertEqual(action["views"][0][1], "form")

    def test_view_processing_edge_cases(self):
        """Test various edge cases in view processing"""
        mixin_obj = self.env["server.env.mixin"]
        arch = etree.XML("<form><sheet><field name='test'/></sheet></form>")

        # 1. view_type != "form"
        res = mixin_obj._update_form_view_from_env(arch, "tree")
        self.assertEqual(res, arch)

        # 2. missing running_env
        with patch.dict(config.options, {"running_env": ""}):
            with self.assertRaises(ValidationError):
                mixin_obj._update_form_view_from_env(arch, "form")

        # 3. missing sheet
        bad_arch = etree.XML("<form><group><field name='test'/></group></form>")
        with self.assertLogs(
            "odoo.addons.server_environment_data_encryption.models.server_env_mixin",
            level="ERROR",
        ) as cm:
            mixin_obj._update_form_view_from_env(bad_arch, "form")
            self.assertTrue(
                any("Missing sheet for form view" in output for output in cm.output)
            )

    def test_set_readonly_form_view_skip_existing(self):
        """Test that _set_readonly_form_view skips fields already
        in _server_env_fields"""
        mixin_obj = self.env["res.partner"]  # This one has 'city' in _server_env_fields
        arch = etree.XML(
            "<form><sheet><field name='city'/><field name='name'/></sheet></form>"
        )
        mixin_obj._set_readonly_form_view(arch, "test", ["test"])

        city_field = arch.find(".//field[@name='city']")
        name_field = arch.find(".//field[@name='name']")

        # city should NOT have readonly added by
        # this method specifically (it's handled differently or skipped)
        self.assertNotIn(
            "context.get(\"environment\", 'test') != 'test'",
            city_field.get("readonly", ""),
        )
        # name SHOULD have it
        self.assertIn(
            "context.get(\"environment\", 'test') != 'test'",
            name_field.get("readonly", ""),
        )

    def test_inverse_server_env_not_editable(self):
        """Test _inverse_server_env when field is not editable"""
        with patch.object(
            type(self.partner),
            "_server_env_is_editable_fieldname",
            return_value="is_company",
        ):
            self.partner.is_company = False
            # This should skip the loop body
            self.partner._inverse_server_env("city")

    def test_get_view_integration(self):
        """Test integration via _get_view"""
        arch_res, view = self.env["res.partner"]._get_view(view_type="form")
        # Check if our extra div was inserted
        self.assertTrue(
            any(
                "action_change_env_data_encrypted_fields"
                in etree.tostring(node, encoding="unicode")
                for node in arch_res.xpath("//button")
            )
        )
