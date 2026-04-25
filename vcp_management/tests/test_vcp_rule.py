# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import os
import tempfile
from unittest.mock import patch

from odoo.exceptions import ValidationError
from odoo.fields import Date

from odoo.addons.base.tests.common import TransactionCase


def _download_code_dummy(self, local_path):
    pass


class TestVcpRules(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.host_type = cls.env["vcp.host.type"].create(
            {
                "name": "Dummy",
                "code": "dummy",
                "code_kind": "dummy",
            }
        )
        cls.host = cls.env["vcp.host"].create(
            {
                "name": "Dummy Platform",
                "type_id": cls.host_type.id,
            }
        )
        # be sure some expected values are set otherwise homepage may fail
        cls.platform = cls.env["vcp.platform"].create(
            {
                "name": "oca",
                "short_description": "OCA",
                "description": "OCA",
                "host_id": cls.host.id,
            }
        )
        cls.repository = cls.env["vcp.repository"].create(
            {
                "name": "contributors-module",
                "description": "OCA/contributors-module",
                "platform_id": cls.platform.id,
                "from_date": Date.today(),
            }
        )
        cls.branch = cls.env["vcp.branch"].create(
            {
                "name": "main",
                "platform_id": cls.platform.id,
            }
        )
        cls.repository_branch = cls.env["vcp.repository.branch"].create(
            {
                "repository_id": cls.repository.id,
                "branch_id": cls.branch.id,
            }
        )
        cls.rule = cls.env["vcp.rule"].create(
            {
                "name": "Test Rule",
                "rule_type": "cloc",
            }
        )

    def setUp(self):
        super().setUp()
        self._tmp_dir = tempfile.TemporaryDirectory(prefix="vcp-git")
        self.env["ir.config_parameter"].sudo().set_param(
            "vcp_management.source_code_local_path", self._tmp_dir.name
        )
        self.addCleanup(self._tmp_dir.cleanup)

    def test_assign_rules(self):
        self.platform.rule_ids = self.rule
        self.assertIn(self.rule, self.repository_branch._get_rules())
        self.repository.override_parent_rules = True
        self.assertNotIn(self.rule, self.repository_branch._get_rules())
        self.repository.rule_ids = self.rule
        self.assertIn(self.rule, self.repository_branch._get_rules())
        self.repository_branch.override_parent_rules = True
        self.assertNotIn(self.rule, self.repository_branch._get_rules())
        self.repository_branch.rule_ids = self.rule
        self.assertIn(self.rule, self.repository_branch._get_rules())

    def test_branch_constrain(self):
        platform = self.env["vcp.platform"].create(
            {
                "name": "test",
                "short_description": "Test",
                "description": "Test",
                "host_id": self.host.id,
            }
        )
        repository = self.env["vcp.repository"].create(
            {
                "name": "test-repo",
                "description": "Test/test-repo",
                "platform_id": platform.id,
                "from_date": Date.today(),
            }
        )
        with self.assertRaises(ValidationError):
            self.env["vcp.repository.branch"].create(
                {
                    "repository_id": repository.id,
                    "branch_id": self.branch.id,
                }
            )

    def test_process_rules(self):
        self.platform.rule_ids = self.rule
        self.assertFalse(os.path.exists(self.repository_branch.local_path))
        self.assertFalse(self.repository_branch.rule_information_ids)
        with (
            patch(
                "odoo.addons.vcp_management.models.vcp_repository_branch.VcpRepositoryBranch._download_code_dummy",
                _download_code_dummy,
                create=True,
            ),
        ):
            os.makedirs(self.repository_branch.local_path, exist_ok=True)
            with open(f"{self.repository_branch.local_path}/demofile.py", "w") as f:
                f.write("""
print('Hello World')

# This is a comment

print('Bye bye world')
""")
            self.repository_branch.process_rules()
        self.repository_branch.invalidate_recordset()
        self.assertTrue(self.repository_branch.rule_information_ids)
        rule_info = self.repository_branch.rule_information_ids.filtered(
            lambda x: x.rule_id == self.rule
        )
        self.assertEqual(rule_info.scanned_files, 1)
        self.assertEqual(rule_info.code_count, 2)
        self.assertEqual(rule_info.documentation_count, 1)
        self.assertEqual(rule_info.empty_count, 3)
        self.assertEqual(rule_info.total_count, 6)

    def test_process_rules_update(self):
        self.platform.rule_ids = self.rule
        self.assertFalse(os.path.exists(self.repository_branch.local_path))
        self.assertFalse(self.repository_branch.rule_information_ids)
        with (
            patch(
                "odoo.addons.vcp_management.models.vcp_repository_branch.VcpRepositoryBranch._download_code_dummy",
                _download_code_dummy,
                create=True,
            ),
        ):
            os.makedirs(self.repository_branch.local_path, exist_ok=True)
            with open(f"{self.repository_branch.local_path}/demofile.py", "w") as f:
                f.write("""
print('Hello World')

# This is a comment

print('Bye bye world')
""")
            self.repository_branch.process_rules()
        self.repository_branch.invalidate_recordset()
        self.assertTrue(self.repository_branch.rule_information_ids)
        rule_info = self.repository_branch.rule_information_ids.filtered(
            lambda x: x.rule_id == self.rule
        )
        self.assertEqual(rule_info.scanned_files, 1)
        self.assertEqual(rule_info.code_count, 2)
        self.assertEqual(rule_info.documentation_count, 1)
        self.assertEqual(rule_info.empty_count, 3)
        self.assertEqual(rule_info.total_count, 6)

    def test_process_rules_only_one_cloc_execution(self):
        rule = self.env["vcp.rule"].create(
            {
                "name": "Test Rule with cloc response",
                "rule_type": "cloc",
                "paths": "*.js",
            }
        )
        self.rule.paths = "*.py"
        self.platform.rule_ids = rule | self.rule
        self.assertFalse(os.path.exists(self.repository_branch.local_path))
        self.assertFalse(self.repository_branch.rule_information_ids)
        with (
            patch(
                "odoo.addons.vcp_management.models.vcp_repository_branch.VcpRepositoryBranch._download_code_dummy",
                _download_code_dummy,
                create=True,
            ),
            patch(
                "odoo.addons.vcp_management.models.vcp_rule.VcpRule._call_cloc_command"
            ) as mock_cloc,
        ):
            mock_cloc.return_value = {
                f"{self.repository_branch.local_path}/demofile.py": {
                    "code": 2,
                    "comment": 1,
                    "empty": 2,
                    "total": 6,
                    "blank": 0,
                },
                f"{self.repository_branch.local_path}/demofile.js": {
                    "code": 1,
                    "comment": 0,
                    "empty": 0,
                    "total": 1,
                    "blank": 0,
                },
            }
            os.makedirs(self.repository_branch.local_path, exist_ok=True)
            with open(f"{self.repository_branch.local_path}/demofile.py", "w") as f:
                f.write("""
# This is a comment
print('Hello World')
print('Hello World')
""")
            with open(f"{self.repository_branch.local_path}/demofile.js", "w") as f:
                f.write("console.log('Hello World');")
            self.repository_branch.process_rules()
            mock_cloc.assert_called_once()
        self.repository_branch.invalidate_recordset()
        self.assertEqual(2, len(self.repository_branch.rule_information_ids))
        self.assertEqual(
            1,
            self.repository_branch.rule_information_ids.filtered(
                lambda x: x.rule_id == rule
            ).code_count,
        )
        self.assertEqual(
            2,
            self.repository_branch.rule_information_ids.filtered(
                lambda x: x.rule_id == self.rule
            ).code_count,
        )
