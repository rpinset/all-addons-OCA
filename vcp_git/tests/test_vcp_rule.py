# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import os
import tempfile
from unittest.mock import MagicMock, patch

from odoo.fields import Date

from odoo.addons.base.tests.common import TransactionCase


class TestVcpRules(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.host_type = cls.env["vcp.host.type"].create(
            {
                "name": "Dummy",
                "code": "dummy",
                "code_kind": "git",
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

    def test_process_rules(self):
        self.platform.rule_ids = self.rule
        self.assertFalse(os.path.exists(self.repository_branch.local_path))
        self.assertFalse(self.repository_branch.rule_information_ids)
        with (
            patch(
                "odoo.addons.vcp_git.models.vcp_platform.VcpPlatform._get_git_url"
            ) as mock_git_url,
            patch(
                "odoo.addons.vcp_git.models.vcp_repository_branch.git.Repo.clone_from"
            ) as mock_clone_from,
        ):
            os.makedirs(self.repository_branch.local_path, exist_ok=True)
            with open(f"{self.repository_branch.local_path}/demofile.py", "w") as f:
                f.write("""
print('Hello World')

# This is a comment

print('Bye bye world')
""")
            self.repository_branch.process_rules()
            mock_git_url.assert_called_once()
            mock_clone_from.assert_called_once()
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
                "odoo.addons.vcp_git.models.vcp_platform.VcpPlatform._get_git_url"
            ) as mock_git_url,
            patch(
                "odoo.addons.vcp_git.models.vcp_repository_branch.git.Repo"
            ) as mock_git_repo,
        ):
            mock_git_url.return_value = "https://example.com/repo.git"
            os.makedirs(self.repository_branch.local_path, exist_ok=True)
            with open(f"{self.repository_branch.local_path}/demofile.py", "w") as f:
                f.write("""
print('Hello World')

# This is a comment

print('Bye bye world')
""")

            mock_git_repo.return_value.remotes = [
                MagicMock(name="origin", url="https://example.com/repo.git")
            ]
            self.repository_branch.process_rules()
            mock_git_url.assert_called_once()
            mock_git_repo.assert_called_once()
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
