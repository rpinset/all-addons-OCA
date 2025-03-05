# © 2014-2015 Tecnativa S.L. - Jairo Llopis
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    department_id = fields.Many2one("res.partner.department", "Department")


class ResPartnerDepartment(models.Model):
    _name = "res.partner.department"
    _order = "display_name"
    _parent_store = True
    _description = "Department"

    name = fields.Char(required=True, translate=True)
    display_name = fields.Char(compute="_compute_display_name", store=True, index=True)
    parent_id = fields.Many2one(
        "res.partner.department", "Parent department", ondelete="restrict"
    )
    child_ids = fields.One2many(
        "res.partner.department", "parent_id", "Child departments"
    )
    parent_path = fields.Char(index=True, unaccent=False)

    @api.depends("parent_path", "name")
    def _compute_display_name(self):
        return super()._compute_display_name()

    def name_get(self):
        """Prepend parent name to department name."""
        all_ids = set(
            map(int, "/".join(rec.parent_path.strip("/") for rec in self).split("/"))
        )
        names = {rec.id: rec.name for rec in self.browse(all_ids)}
        return [
            (
                rec.id,
                " / ".join(
                    names[int(id)] for id in rec.parent_path.strip("/").split("/")
                ),
            )
            for rec in self
        ]
