# Copyright 2020 ACSONE SA
# @author Simone Orsi <simahawk@gmail.com>
# Copyright 2021 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class EDIBackend(models.Model):
    _inherit = "edi.backend"

    def _register_hook(self):
        self._patch_method(
            "_storage_create_record_if_missing",
            self._patch_job_auto_delay("_storage_create_record_if_missing"),
        )
        return super()._register_hook()
