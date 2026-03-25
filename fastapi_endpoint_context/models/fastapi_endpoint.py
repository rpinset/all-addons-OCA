# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models

from odoo.addons.fastapi import dependencies

from ..dependencies import odoo_env_with_context


class FastapiEndpoint(models.Model):
    _inherit = "fastapi.endpoint"

    def _get_app_context(self):
        """Add the fastapi app and endpoint id to the odoo env context"""
        return {
            "fastapi_app": self.app,
            "fastapi_endpoint_id": self.id,
        }

    def _get_app_dependencies_overrides(self):
        res = super()._get_app_dependencies_overrides()
        res.update({dependencies.odoo_env: odoo_env_with_context})
        return res
