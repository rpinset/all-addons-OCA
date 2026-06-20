# Copyright (C) 2022 Trevi Software (https://trevi.et)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrJob(models.Model):

    _inherit = "hr.job"

    ethiopic_name = fields.Char()

    def name_get(self):

        res = []
        use_ethiopic_name = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("l10n_et_hr.use_ethiopic_job_name")
        )
        if use_ethiopic_name:
            for rec in self:
                name = rec.name
                if rec.ethiopic_name:
                    name = rec.ethiopic_name
                res.append((rec.id, name))
            return res

        return super().name_get()
