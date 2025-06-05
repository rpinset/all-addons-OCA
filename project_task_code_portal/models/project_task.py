# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS | {"code"}
