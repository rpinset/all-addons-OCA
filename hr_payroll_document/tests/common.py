# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import contextlib
from unittest import mock

from odoo.modules.module import get_module_resource
from odoo.tests import common

from odoo.addons.mail.tests.common import mail_new_test_user


class TestHrPayrollDocument(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.env.user.tz = "Europe/Brussels"
        self.user_admin = self.env.ref("base.user_admin")

        # Fix Company without country
        self.env.company.country_id = False

        # Test users to use through the various tests
        self.user_employee = mail_new_test_user(
            self.env, login="david", groups="base.group_user"
        )
        self.user_employee_id = self.user_employee.id

        # Hr Data
        self.employee_emp = self.env["hr.employee"].create(
            {
                "name": "David Employee",
                "user_id": self.user_employee_id,
                "company_id": 1,
                "identification_id": "30831011V",
            }
        )

        self.wizard = self._create_wizard(
            "January", ["hr_payroll_document", "tests", "test.pdf"]
        )

    def _create_wizard(self, subject, file_path):
        with open(get_module_resource(*file_path), "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        ir_values = {
            "name": "test",
            "type": "binary",
            "datas": encoded_string,
            "store_fname": encoded_string,
            "res_model": "payroll.management.wizard",
            "res_id": 1,
        }
        self.attachment = self.env["ir.attachment"].create(ir_values)
        self.subject = subject
        return self.env["payroll.management.wizard"].create(
            {"payrolls": [self.attachment.id], "subject": self.subject}
        )

    @contextlib.contextmanager
    def _mock_valid_identification(self, employee, identification_code):
        def _mocked_validate_payroll_identification(self, code=None):
            if code is None:
                code = employee.identification_id
            return code == identification_code

        with mock.patch.object(
            type(employee),
            "_validate_payroll_identification",
            _mocked_validate_payroll_identification,
        ) as patch:
            patch.side_effect = _mocked_validate_payroll_identification
            yield

    def fill_company_id(self):
        self.env.company.country_id = self.env["res.country"].search(
            [("name", "=", "Spain")]
        )
