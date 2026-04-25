# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError


class VcpOdooBinPackage(models.Model):
    _name = "vcp.odoo.bin.package"
    _description = "Binary Package required by an Odoo Module"

    name = fields.Char(required=True, readonly=True)

    module_version_ids = fields.Many2many(
        "vcp.odoo.module.version",
        string="Odoo Module Versions",
        readonly=True,
    )

    @tools.ormcache("name")
    def _get_bin_package(self, name):
        bin_src = self.search([("name", "=", name)], limit=1)
        if not bin_src:
            bin_src = self.create({"name": name})
        return bin_src.id

    @api.ondelete(at_uninstall=False)
    def _check_module_versions(self):
        if self.mapped("module_version_ids"):
            raise UserError(
                _(
                    "You can not delete packages that are related to Odoo Modules. "
                    "You should first delete the related odoo modules."
                )
            )
