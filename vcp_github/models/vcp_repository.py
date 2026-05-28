# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
import re
from datetime import datetime, timedelta

import github3
from github3 import pulls
from pytz import UTC

from odoo import fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class VcpRepository(models.Model):
    _inherit = "vcp.repository"

    def _get_repository_url(self):
        result = super()._get_repository_url()
        if not result and self.platform_id.host_id.type_id.code == "github":
            return f"https://github.com/{self.platform_id.name}/{self.name}"
        return result

    def _update_branches_github(self):
        self.ensure_one()
        client = self.platform_id._get_github_clients()[0]
        try:
            repo = client.repository(self.platform_id.name, self.name)
            original_branches = self.branch_ids
            existing_branches = {b.branch_id.name: b for b in self.branch_ids}
            found_branches = self.env["vcp.repository.branch"]
            for branch in repo.branches():
                branch_pattern = (
                    self.fetch_branch_pattern
                    or self.platform_id.fetch_repository_branch_pattern
                    or False
                )
                if branch_pattern and not re.match(branch_pattern, branch.name):
                    continue
                if branch.name in existing_branches:
                    existing_branches[branch.name].sudo().write(
                        {"last_commit": branch.commit.sha}
                    )
                    found_branches |= existing_branches[branch.name]
                else:
                    self.env["vcp.repository.branch"].sudo().create(
                        {
                            "repository_id": self.id,
                            "branch_id": self.platform_id._get_branch(branch.name),
                            "last_commit": branch.commit.sha,
                        }
                    )
            (original_branches - found_branches).sudo().unlink()
        except github3.exceptions.ForbiddenError as e:
            _logger.error(e)
            rate = client.rate_limit()
            reset = fields.Datetime.to_string(
                datetime.utcfromtimestamp(rate["resources"]["core"]["reset"])
            )
            raise ValidationError(self.env._(f"Reset on {reset}")) from e

    def _parse_github_pr(self, pr, client):
        self.ensure_one()
        origin_data = pr.as_dict()
        comments_url = pr.comments_url
        comments_req = client.session.get(comments_url)
        comments = comments_req.json()
        while comments_req.links.get("next"):
            comments_url = comments_req.links["next"]["url"]
            comments_req = client.session.get(comments_url)
            comments += comments_req.json()
        reviews_url = pr.reviews().url
        reviews_req = client.session.get(reviews_url)
        reviews = reviews_req.json()
        while reviews_req.links.get("next"):
            reviews_url = reviews_req.links["next"]["url"]
            reviews_req = client.session.get(reviews_url)
            reviews += reviews_req.json()

        branch_pattern = (
            self.fetch_branch_pattern
            or self.platform_id.fetch_repository_branch_pattern
            or False
        )
        if branch_pattern and not re.match(branch_pattern, pr.base.ref):
            branch_id = False
        else:
            branch_id = self.platform_id._get_branch(pr.base.ref)
        return (
            str(pr.id),
            {
                "user_id": self.platform_id.host_id._get_user(pr.user.login),
                "repository_id": self.id,
                "branch_id": branch_id,
                "organization_id": self.platform_id.host_id._get_organization(
                    pr.head.repo[0]
                ),
                "url": pr.html_url,
                "state": pr.state,
                "name": pr.title,
                "is_merged": any(label["name"] == "merged 🎉" for label in pr.labels)
                or pr.is_merged(),
                "is_draft": pr.draft,
                "created_at": self.platform_id._parse_github_date(
                    origin_data["created_at"]
                ),
                "closed_at": self.platform_id._parse_github_date(
                    origin_data["closed_at"]
                ),
                "number": pr.number,
                "updated_at": self.platform_id._parse_github_date(
                    origin_data["updated_at"]
                ),
                "label_ids": [fields.Command.clear()]
                + [
                    fields.Command.link(
                        self.env["vcp.request.label"]._get_label(label["name"])
                    )
                    for label in origin_data["labels"]
                ],
                "commits": origin_data["commits"],
                "total_comments": origin_data["comments"],
                "review_comments": origin_data["review_comments"],
                "additions": origin_data["additions"],
                "deletions": origin_data["deletions"],
            },
            [
                {
                    "id": str(c["id"]),
                    "user_id": c.get("user")
                    and self.platform_id.host_id._get_user(c["user"].get("login")),
                    "body": self.platform_id._parse_github_markdown(c["body"]),
                    "created_at": self.platform_id._parse_github_date(c["created_at"]),
                    "updated_at": self.platform_id._parse_github_date(c["updated_at"]),
                }
                for c in comments
            ],
            [
                {
                    "id": str(r["id"]),
                    "user_id": r.get("user")
                    and self.platform_id.host_id._get_user(r["user"].get("login")),
                    "body": self.platform_id._parse_github_markdown(r["body"]),
                    "submitted_at": self.platform_id._parse_github_date(
                        r.get("submitted_at")
                    ),
                    "state": r["state"]["keyword"]
                    if isinstance(r["state"], dict)
                    else r["state"],
                }
                for r in reviews
            ],
        )

    def _update_information_github(
        self, update_interval_days=None, client_for_search=0
    ):
        self.ensure_one()
        clients = self.platform_id._get_github_clients()
        try:
            start = UTC.localize(self.from_date)
            end = min(
                start
                + timedelta(
                    days=update_interval_days or self.platform_id.update_interval_days
                ),
                UTC.localize(datetime.now()),
            )
            start += timedelta(
                days=-1
            )  # Add buffer day to avoid missing PRs on boundary dates
            i = client_for_search % len(clients)
            for pr in clients[i].search_issues(
                f"is:pr repo:{self.platform_id.name}/{self.name} "
                f"updated:{start.isoformat()}..{end.isoformat()}"
            ):
                i = (1 + i) % len(clients)
                pr_id, pr_data, comments, reviews = self._parse_github_pr(
                    clients[i]._instance_or_null(
                        pulls.PullRequest,
                        clients[i]._json(
                            pr.issue._get(pr.issue.pull_request_urls.get("url")), 200
                        ),
                    ),
                    clients[i],
                )
                opr = self.env["vcp.request"].search(
                    [("external_id", "=", pr_id), ("repository_id", "=", self.id)],
                    limit=1,
                )
                if not opr:
                    opr = (
                        self.env["vcp.request"]
                        .sudo()
                        .create({"external_id": pr_id, **pr_data})
                    )
                else:
                    opr.sudo().write(pr_data)
                for comment in comments:
                    comment_id = comment.pop("id")
                    ocomment = self.env["vcp.comment"].search(
                        [
                            ("external_id", "=", comment_id),
                            ("repository_id", "=", self.id),
                        ],
                        limit=1,
                    )
                    if not ocomment:
                        self.env["vcp.comment"].sudo().create(
                            {
                                "external_id": comment_id,
                                "request_id": opr.id,
                                **comment,
                            }
                        )
                    else:
                        ocomment.sudo().write(comment)
                for review in reviews:
                    review_id = review.pop("id")
                    oreview = self.env["vcp.review"].search(
                        [
                            ("external_id", "=", review_id),
                            ("repository_id", "=", self.id),
                        ],
                        limit=1,
                    )
                    if not oreview:
                        self.env["vcp.review"].sudo().create(
                            {
                                "external_id": review_id,
                                "request_id": opr.id,
                                **review,
                            }
                        )
                    else:
                        oreview.sudo().write(review)
            self.sudo().from_date = end.replace(tzinfo=None)
        except github3.exceptions.ForbiddenError as e:
            _logger.error(e)
            rate = clients[i].rate_limit()
            reset = fields.Datetime.to_string(
                datetime.utcfromtimestamp(rate["resources"]["core"]["reset"])
            )
            raise ValidationError(self.env._(f"Reset on {reset}")) from e
