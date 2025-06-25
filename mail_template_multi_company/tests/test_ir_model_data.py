# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import AccessError
from odoo.tests import SavepointCase

from odoo.addons.mail.tests.common import mail_new_test_user


class TestIRModelData(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.other_company = cls.env["res.company"].create(
            {
                "name": "Test other Company",
            }
        )

        cls.other_company_template = cls.env["mail.template"].create(
            {
                "name": "Test other company template",
                "company_id": cls.other_company.id,
            }
        )
        cls.other_company_template_data = cls.env["ir.model.data"].create(
            {
                "module": "test_module",
                "name": "test_xmlid",
                "model": cls.other_company_template._name,
                "res_id": cls.other_company_template.id,
            }
        )
        cls.other_company_template_xmlid = ".".join(
            [
                cls.other_company_template_data.module,
                cls.other_company_template_data.name,
            ]
        )

        company_user = mail_new_test_user(
            cls.env,
            login="Test company user",
            company_id=cls.company.id,
            company_ids=cls.company.ids,
        )

        cls.env = cls.env(user=company_user)
        cls.cr = cls.env.cr

    def test_ref_xmlid_not_found(self):
        """
        When a template is found by XMLID but is in another company,
        behave as if it wasn't found.
        """
        # Arrange
        company = self.env.company
        template_sudo = self.env(su=True).ref(self.other_company_template_xmlid)
        # pre-condition
        self.assertTrue(template_sudo)
        self.assertNotEqual(template_sudo.company_id, company)

        # Act
        with self.assertRaises(AccessError) as ae:
            self.env.ref(self.other_company_template_xmlid, raise_if_not_found=True)
        exc_message = ae.exception.args[0]
        template = self.env.ref(
            self.other_company_template_xmlid, raise_if_not_found=False
        )

        # Assert
        self.assertIn("Not enough access rights", exc_message)
        self.assertFalse(template)

    def test_substitute(self):
        """
        When a template is not found by XMLID but has a substitute,
        the substitute is found instead.
        """
        # Arrange
        company = self.env.company
        other_company_template = self.other_company_template
        copied_other_company_template = other_company_template.copy(
            default={
                "company_id": company.id,
            },
        )
        # pre-condition
        self.assertEqual(
            copied_other_company_template.original_xmlid_mail_template_id,
            other_company_template,
        )

        # Act
        template = self.env.ref(
            self.other_company_template_xmlid, raise_if_not_found=False
        )

        # Assert
        self.assertEqual(template, copied_other_company_template)

    def test_only_access_rule(self):
        """If a user has no access rights to email templates,
        do not raise an AccessError.
        """
        # Arrange
        user = self.env.ref("base.demo_user0")
        user_env = self.env(user=user)
        # pre-condition
        self.assertFalse(
            user_env["ir.model.access"].check(
                "mail.template",
                "read",
                raise_exception=False,
            )
        )

        # Act
        template = user_env.ref(
            self.other_company_template_xmlid, raise_if_not_found=False
        )

        # Assert
        self.assertTrue(template)
