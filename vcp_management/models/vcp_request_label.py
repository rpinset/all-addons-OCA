# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from random import randint

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError


class VcpRequestLabel(models.Model):
    _name = "vcp.request.label"
    _description = "Vcp Request Label"

    name = fields.Char(required=True, readonly=True)

    color = fields.Char(default=lambda x: x._default_color())

    request_ids = fields.Many2many(
        comodel_name="vcp.request",
        string="Requests",
        readonly=True,
    )

    _sql_constraints = [("name_uniq", "unique(name)", "Label name must be unique.")]

    def _default_color(self):
        return randint(1, 11)

    @tools.ormcache("name")
    def _get_label(self, name):
        label = self.search([("name", "=", name)], limit=1)
        if not label:
            label = self.sudo().create({"name": name})
        return label.id

    @api.ondelete(at_uninstall=False)
    def _check_requests(self):
        if self.mapped("request_ids"):
            raise UserError(
                _(
                    "You can not delete labels that are related to Requests. "
                    "You should first delete the related requests."
                )
            )
