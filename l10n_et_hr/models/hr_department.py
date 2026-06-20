# Copyright (C) 2022 Trevi Software (https://trevi.et)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class HrDepartment(models.Model):

    _inherit = "hr.department"

    ethiopic_name = fields.Char()

    def name_get(self):

        res = []
        use_ethiopic_name = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("l10n_et_hr.use_ethiopic_department_name")
        )
        if use_ethiopic_name and not self.env.context.get("hierarchical_naming", True):
            for rec in self:
                name = rec.name
                if rec.ethiopic_name:
                    name = rec.ethiopic_name
                res.append((rec.id, name))
            return res

        return super().name_get()

    @api.depends("name", "ethiopic_name", "parent_id.complete_name")
    def _compute_complete_name(self):

        use_ethiopic_name = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("l10n_et_hr.use_ethiopic_department_name")
        )
        if use_ethiopic_name:
            for department in self:
                name = department.name
                if department.ethiopic_name:
                    name = department.ethiopic_name
                if department.parent_id:
                    department.complete_name = "%s / %s" % (
                        department.parent_id.complete_name,
                        name,
                    )
                else:
                    department.complete_name = name
        else:
            super()._compute_complete_name()
