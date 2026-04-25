# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
from unittest.mock import MagicMock, patch

from odoo.fields import Command
from odoo.tests.common import TransactionCase


class TestGithub(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.platform = cls.env["vcp.platform"].create(
            {
                "name": "oca",
                "host_id": cls.env.ref("vcp_github.vcp_github_host").id,
                "key_ids": [
                    Command.create({"name": "ghp_exampletoken1234567890abcdef"})
                ],
                "default_repository_scheduled_information_update": True,
                "scheduled_information_update": True,
            }
        )

    def test_update_organization_and_logo(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        with (
            patch("odoo.addons.vcp_github.models.vcp_platform.github3") as mock_github3,
            patch(
                "odoo.addons.vcp_github.models.vcp_platform.requests.get"
            ) as mock_requests_get,
        ):
            mock_client = MagicMock()
            mock_org = MagicMock()
            mock_org.name = "Odoo Community Association"
            mock_org.avatar_url = f"{base_url}/logo.png"
            mock_requests_get.return_value.content = base64.b64decode(
                self.env.company.logo
            )
            mock_client.organization.return_value = mock_org
            mock_github3.login.return_value = mock_client
            self.platform.update_information()
            self.assertEqual(
                self.platform.short_description, "Odoo Community Association"
            )
            mock_github3.login.assert_called_once_with(
                token="ghp_exampletoken1234567890abcdef"
            )
            mock_client.organization.assert_called_once_with("oca")

    def test_update_organization_with_repository(self):
        with patch(
            "odoo.addons.vcp_github.models.vcp_platform.github3"
        ) as mock_github3:
            mock_client = MagicMock()
            mock_org = MagicMock()
            mock_org.name = "Odoo Community Association"
            mock_org.avatar_url = False
            mock_repo1 = MagicMock()
            mock_repo1.name = "server-tools"
            mock_repo1.archived = False
            mock_repo1.fork = False
            mock_repo1.created_at = "2020-01-01T00:00:00Z"
            mock_repo1.pushed_at = "2020-02-01T00:00:00Z"
            mock_repo2 = MagicMock()
            mock_repo2.name = "server-brand"
            mock_repo2.archived = False
            mock_repo2.fork = False
            mock_repo2.created_at = "2021-01-01T10:00:00Z"
            mock_repo2.pushed_at = "2021-02-01T00:00:00Z"
            mock_org.repositories.return_value = [mock_repo1, mock_repo2]
            mock_client.organization.return_value = mock_org
            mock_github3.login.return_value = mock_client
            self.platform.update_information()
            self.assertEqual(len(self.platform.repository_ids), 2)
            repo_names = {repo.name for repo in self.platform.repository_ids}
            self.assertSetEqual(repo_names, {"server-tools", "server-brand"})
            mock_github3.login.assert_called_once_with(
                token="ghp_exampletoken1234567890abcdef"
            )
            mock_client.organization.assert_called_once_with("oca")
        return self.platform.repository_ids.filtered(lambda r: r.name == "server-tools")

    def test_update_repository(self):
        repository = self.test_update_organization_with_repository()
        self.assertFalse(repository.request_ids)
        with patch(
            "odoo.addons.vcp_github.models.vcp_platform.github3.login"
        ) as mock_client:
            mock_login = MagicMock()
            mock_client.return_value = mock_login
            mock_login.session.get.return_value = MagicMock(
                links={},
                json=lambda: [],
            )
            mock_issue_request = MagicMock(
                as_dict=lambda: {
                    "id": 1,
                    "user": {"login": "contributor1"},
                    "base": {"ref": "main"},
                    "head": {"repo": [MagicMock()]},
                    "html_url": "https://github.com/oca/server-tools/pull/1",
                    "state": "closed",
                    "title": "Fix issue",
                    "labels": [{"name": "merged 🎉"}],
                    "created_at": "2023-01-01T00:00:00Z",
                    "updated_at": "2023-01-03T00:00:00Z",
                    "closed_at": "2023-01-02T00:00:00Z",
                    "pushed_at": "2024-01-02T00:00:00Z",
                    "commits": 3,
                    "comments": 2,
                    "review_comments": 1,
                    "additions": 150,
                    "deletions": 50,
                    "number": 1,
                }
            )
            mock_login._instance_or_null.return_value = mock_issue_request
            mock_login.search_issues.return_value = [mock_issue_request]
            repository.update_information()
        self.assertTrue(repository.request_ids)
