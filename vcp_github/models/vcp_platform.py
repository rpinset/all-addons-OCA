# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
from datetime import datetime

import github3
import markdown
import requests
from pytz import UTC

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class VcpPlatform(models.Model):
    _inherit = "vcp.platform"

    def _get_git_url_github(self, repository):
        return f"https://github.com/{self.name}/{repository.name}"

    def _get_github_clients(self):
        git = []
        for key in self.key_ids:
            git.append(github3.login(token=key.name))
        return git

    def _update_information_github(self):
        self.ensure_one()
        clients = self._get_github_clients()
        if not clients:
            raise ValidationError(
                _(
                    "No github clients configured. "
                    "Please enter at least a Github Personal Access Token. "
                    "You can check more information at "
                    "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens"
                )
            )
        org = clients[0].organization(self.name)
        self.short_description = org.name
        self.description = org.description
        if org.avatar_url:
            response = requests.get(org.avatar_url, timeout=10)
            response.raise_for_status()
            self.image_1920 = base64.b64encode(response.content)
        repos = org.repositories()
        for repo in repos:
            if repo.fork and not self.fetch_repository_fork:
                continue
            if repo.archived and not self.fetch_repository_archived:
                continue
            self._update_github_repository(repo)
        self.last_update = fields.Datetime.now()

    def _parse_github_date(self, date):
        if not date:
            return False
        return UTC.normalize(
            datetime.fromisoformat(date.replace("Z", "+00:00"))
        ).replace(tzinfo=None)

    def _parse_github_markdown(self, text):
        return markdown.markdown(text)

    def _update_github_repository(self, repo):
        vals = {
            "created_at": self._parse_github_date(repo.created_at),
            "last_commit_date": self._parse_github_date(repo.pushed_at),
            "stargazers_count": repo.stargazers_count,
            "fork_count": repo.forks_count,
            "is_fork": repo.fork,
            "active": not repo.archived,
            "watchers_count": repo.watchers_count,
            "description": repo.description,
        }
        repository = (
            self.env["vcp.repository"]
            .with_context(active_test=False)
            .search(
                [
                    ("name", "=", repo.name),
                    ("platform_id", "=", self.id),
                ],
                limit=1,
            )
        )
        if not repository:
            repository = (
                self.env["vcp.repository"]
                .sudo()
                .create(
                    {
                        "name": repo.name,
                        "platform_id": self.id,
                        "from_date": vals.get("created_at"),
                        **vals,
                    }
                )
            )
        else:
            repository.sudo().write(vals)
