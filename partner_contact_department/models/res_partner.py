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
    display_name = fields.Char(
        compute="_compute_display_name",
        store=True,
        index=True,
        translate=True,
        recursive=True,
    )
    parent_id = fields.Many2one(
        "res.partner.department", "Parent department", ondelete="restrict"
    )
    child_ids = fields.One2many(
        "res.partner.department", "parent_id", "Child departments"
    )
    parent_path = fields.Char(index=True, unaccent=False)

    @api.depends("parent_path", "parent_id.display_name", "name")
    def _compute_display_name(self):
        # Avoid computing multiple languages if record is not yet saved
        if not self.ids:
            return super()._compute_display_name()
        # When record is in DB, update display name in all languages
        for lang, _name in self.env["res.lang"].get_installed():
            _self = self.with_context(lang=lang)
            super(ResPartnerDepartment, _self)._compute_display_name()
        return True

    def name_get(self):
        """Prepend parent name to department name."""
        result = super().name_get()
        for position, ((id_, name), rec) in enumerate(zip(result, self)):
            while rec.parent_id.name:
                name = f"{rec.parent_id.name} / {name}"
                rec = rec.parent_id
            result[position] = (id_, name)
        return result
