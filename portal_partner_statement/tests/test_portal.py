# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import requests

from odoo import tests

from odoo.addons.account.tests.common import AccountTestInvoicingHttpCommon


@tests.tagged("post_install", "-at_install")
class TestPortal(AccountTestInvoicingHttpCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.outstanding_group = cls.env.ref(
            "partner_statement.group_outstanding_statement"
        )
        cls.base_group = cls.env.ref("account.group_account_invoice")
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test partner",
                "email": "a@b.c",
                "company_id": cls.env.company.id,
            }
        )
        cls.invoice = cls.init_invoice(
            "out_invoice",
            partner=cls.partner,
            amounts=[100],
            post=True,
        )

    def _grant_portal_access(self, partners):
        wizard = (
            self.env["portal.wizard"]
            .with_context(
                active_ids=partners.ids,
            )
            .create({})
        )
        wizard.user_ids.in_portal = True
        result = wizard.action_apply()
        # For easier authentication,
        # set password = login for each created user
        for user in partners.user_ids:
            user.password = user.login
        return result

    def _activate_group(self, group):
        self.base_group.implied_ids |= group

    def _is_group_active(self, group):
        return group in self.base_group.implied_ids

    def _download_report_url(self, report_name, report_type):
        return (
            "/my/partner_statements/download?"
            f"report_name={report_name}"
            f"&report_type={report_type}"
        )

    def test_outstanding_not_allowed(self):
        """
        If the outstanding statement is not enabled with security groups,
        the report cannot be downloaded.
        """
        # Arrange
        partner = self.partner
        self._grant_portal_access(partner)
        partner_user = partner.user_ids
        outstanding_group = self.outstanding_group
        # pre-condition
        self.assertFalse(self._is_group_active(outstanding_group))
        self.assertEqual(partner, partner.commercial_partner_id)

        # Act
        self.authenticate(partner_user.login, partner_user.login)
        response = self.url_open(
            self._download_report_url("outstanding_statement", "pdf"),
        )

        # Assert
        self.assertEqual(response.status_code, requests.codes.forbidden)

    def test_outstanding_not_allowed_child(self):
        """
        If the outstanding statement is requested from a child partner,
        the report cannot be downloaded.
        """
        # Arrange
        commercial_partner = self.partner
        partner = self.env["res.partner"].create(
            {
                "name": "Child partner",
                "email": "d@e.f",
                "parent_id": commercial_partner.id,
            }
        )
        self._grant_portal_access(partner)
        partner_user = partner.user_ids
        outstanding_group = self.outstanding_group
        self._activate_group(outstanding_group)
        # pre-condition
        self.assertTrue(self._is_group_active(outstanding_group))
        self.assertNotEqual(partner, partner.commercial_partner_id)

        # Act
        self.authenticate(partner_user.login, partner_user.login)
        response = self.url_open(
            self._download_report_url("outstanding_statement", "pdf"),
        )

        # Assert
        self.assertEqual(response.status_code, requests.codes.forbidden)

    def test_download_outstanding(self):
        """
        The report can be downloaded.
        """
        # Arrange
        invoice = self.invoice
        partner = invoice.partner_id
        self._grant_portal_access(partner)
        partner_user = partner.user_ids
        outstanding_group = self.outstanding_group
        self._activate_group(outstanding_group)
        # pre-condition
        self.assertTrue(self._is_group_active(outstanding_group))
        self.assertEqual(partner, partner.commercial_partner_id)

        # Act
        self.authenticate(partner_user.login, partner_user.login)
        response = self.url_open(
            self._download_report_url("outstanding_statement", "pdf"),
        )

        # Assert
        self.assertEqual(response.status_code, requests.codes.ok)
        self.assertIn(invoice.name.encode(), response.content)
