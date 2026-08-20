# Copyright 2026 Vauxoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json
from urllib.parse import quote, urlencode

from odoo.tests.common import tagged

from odoo.addons.web.tests.test_reports import TestReports


@tagged("-at_install", "post_install")
class TestReportQwebEncryptDownload(TestReports):
    """Cover the /report/download override.

    It inherits the core TestReports so its report regression tests also run
    with this module installed. Core has no test hitting /report/download
    itself, so the cases below are new.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.encrypt_report = cls.env.ref("web.action_report_internalpreview")
        # The controller encrypts on its own, using the password found in the
        # url. Keep the model side disabled so each assertion below can only
        # be explained by the controller.
        cls.encrypt_report.encrypt = False
        cls.encrypt_company = cls.env.ref("base.main_company")

    def _report_url(self, context=None):
        """Url of the report as action_manager_report.esm.js builds it"""
        url = f"/report/pdf/{self.encrypt_report.report_name}/{self.encrypt_company.id}"
        if context is not None:
            url += "?context=" + quote(json.dumps(context))
        return url

    def _download(self, url):
        """Call /report/download the way the web client does

        force_report_rendering is required because _render_qweb_pdf() falls
        back to _render_qweb_html() while tests are running, and an html body
        cannot be encrypted.
        """
        params = {
            "data": json.dumps([url, "qweb-pdf"]),
            "context": json.dumps({"force_report_rendering": True}),
        }
        response = self.url_open("/report/download?" + urlencode(params))
        response.raise_for_status()
        self.assertEqual(response.headers.get("Content-Type"), "application/pdf")
        return response

    def test_download_encrypts_with_password_in_url(self):
        """It should encrypt the pdf with the password given in the url"""
        self.authenticate("admin", "admin")
        response = self._download(self._report_url({"encrypt_password": "secretcode"}))
        self.assertIn(b"/Encrypt", response.content)

    def test_download_without_query_string(self):
        """It should return the pdf untouched when the url has no context"""
        self.authenticate("admin", "admin")
        response = self._download(self._report_url())
        self.assertNotIn(b"/Encrypt", response.content)

    def test_download_without_password_in_context(self):
        """It should return the pdf untouched when no password is given"""
        self.authenticate("admin", "admin")
        response = self._download(self._report_url({"lang": "en_US"}))
        self.assertNotIn(b"/Encrypt", response.content)

    def test_download_non_pdf_response_untouched(self):
        """It should not touch a response that is not a pdf

        report_download() also serves qweb-text reports; the override has to
        let anything that is not application/pdf go through untouched.
        """
        self.authenticate("admin", "admin")
        context = quote(json.dumps({"encrypt_password": "secretcode"}))
        url = (
            f"/report/text/{self.encrypt_report.report_name}"
            f"/{self.encrypt_company.id}?context={context}"
        )
        params = {
            "data": json.dumps([url, "qweb-text"]),
            "context": json.dumps({"force_report_rendering": True}),
        }
        response = self.url_open("/report/download?" + urlencode(params))
        response.raise_for_status()
        self.assertNotEqual(response.headers.get("Content-Type"), "application/pdf")
        self.assertNotIn(b"/Encrypt", response.content)
