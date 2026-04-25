# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools


class VcpOdooModule(models.Model):
    _name = "vcp.odoo.module"
    _description = "Odoo Module"

    name = fields.Char(required=True, readonly=True)
    version_ids = fields.One2many(
        "vcp.odoo.module.version", inverse_name="module_id", readonly=True
    )
    version_count = fields.Integer(
        compute="_compute_version_count",
        help="number of versions in which the module is available",
        store=True,
    )
    repository_branch_ids = fields.Many2many(
        "vcp.repository.branch", compute="_compute_repository_branch_ids"
    )

    _sql_constraints = [
        ("name_uniq", "unique(name)", "The module name must be unique"),
    ]

    @api.depends("version_ids")
    def _compute_version_count(self):
        for record in self:
            record.version_count = len(record.version_ids)

    @api.depends("version_ids.repository_branch_id")
    def _compute_repository_branch_ids(self):
        for record in self:
            record.repository_branch_ids = record.mapped(
                "version_ids.repository_branch_id"
            ).sorted(lambda x: x.branch_id.name)

    @tools.ormcache("name")
    def _get_odoo_module(self, name):
        """
        Get the Odoo module with the given name, creating it if it doesn't exist.
        """
        module = self.search(
            [("name", "=", name)],
            limit=1,
        )
        if not module:
            module = self.env["vcp.odoo.module"].create({"name": name})
        return module.id
