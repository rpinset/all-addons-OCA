# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import git

from odoo import models


class VcpRepositoryBranch(models.Model):
    _inherit = "vcp.repository.branch"

    def _download_code_git(self, local_path):
        try:
            repo = git.Repo(local_path)
            for remote in repo.remotes:
                if remote.url == self.repository_id._get_git_url():
                    remote.fetch(self.branch_id.name)
                    repo.git.reset("--hard", f"{remote.name}/{self.branch_id.name}")
                    break
        except git.exc.InvalidGitRepositoryError:
            # Not cloned yet
            repo = git.Repo.clone_from(
                self.repository_id._get_git_url(),
                local_path,
                branch=self.branch_id.name,
                depth=1,
            )
