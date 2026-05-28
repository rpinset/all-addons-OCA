# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


import logging
from datetime import datetime

import github3

from odoo import fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class VcpUser(models.Model):
    _inherit = "vcp.user"

    def _get_contributor_url(self):
        result = super()._get_contributor_url()
        if not result and self.host_id.type_id.code == "github":
            return f"https://github.com/{self.external_id}"
        return result

    def _prepare_user_vals(self, user):
        return {
            "name": user.name or user.login,
            "email": user.email,
            "avatar_url": user.avatar_url,
            "company": user.company,
        }

    def _update_information_github(self):
        self.ensure_one()
        # TODO maybe we should move the api key on the host ?
        platform = self.env["vcp.platform"].search(
            [("host_id", "=", self.host_id.id)], limit=1
        )
        client = platform._get_github_clients()[0]
        try:
            user = client.user(self.external_id)
            self.write(self._prepare_user_vals(user))
        except github3.exceptions.ForbiddenError as e:
            _logger.error(e)
            rate = client.rate_limit()
            reset = fields.Datetime.to_string(
                datetime.utcfromtimestamp(rate["resources"]["core"]["reset"])
            )
            raise ValidationError(self.env._(f"Reset on {reset}")) from e
        except github3.exceptions.NotFoundError:
            _logger.warning(
                "The user %s do not exist anymore, inactive it", self.external_id
            )
            self.active = False
