# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

import json

from odoo.tests.common import HttpCase


class TestReportDocxController(HttpCase):
    def test_demo_reports(self):
        self.authenticate("admin", "admin")
        result = self.opener.get(
            self.base_url() + "/report_docx",
            data=dict(
                report_name="ir_module_multi_mode_zip",
                ids=json.dumps(self.env.ref("base.module_report_docx").ids),
            ),
        )
        self.assertEqual(
            result.headers["content-type"],
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
