# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VcpOdooModuleVersion(models.Model):
    _name = "vcp.odoo.module.version"
    _description = "Odoo Module on an specific repository branch"
    _inherit = ["vcp.rule.information.mixin", "image.mixin"]

    name = fields.Char(required=True, readonly=True)
    path = fields.Char(required=True, readonly=True)
    module_id = fields.Many2one(
        "vcp.odoo.module",
        readonly=True,
        required=True,
        ondelete="cascade",
    )
    version = fields.Char(
        required=True,
        readonly=True,
    )
    repository_branch_id = fields.Many2one(
        "vcp.repository.branch",
        readonly=True,
        required=True,
        ondelete="cascade",
    )
    depends_on_module_ids = fields.Many2many(
        "vcp.odoo.module",
        readonly=True,
    )
    auto_install = fields.Boolean(readonly=True)
    license = fields.Char(string="License (Manifest)", readonly=True)
    summary = fields.Char(string="Summary (Manifest)", readonly=True)
    website = fields.Char(string="Website (Manifest)", readonly=True)
    python_library_ids = fields.Many2many(
        "vcp.odoo.python.library",
        string="Python Libraries",
        readonly=True,
    )
    bin_package_ids = fields.Many2many(
        "vcp.odoo.bin.package",
        string="Python Binaries",
        readonly=True,
    )
    description = fields.Html(readonly=True)

    def _get_local_path(self):
        return f"{self.repository_branch_id.local_path}/{self.path}"
