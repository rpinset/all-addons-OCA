# Copyright (C) 2022 Trevi Software (https://trevi.et)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    use_ethiopic_name = fields.Boolean(
        config_parameter="l10n_et_hr.use_ethiopic_employee_name"
    )
    use_ethiopic_department = fields.Boolean(
        config_parameter="l10n_et_hr.use_ethiopic_department_name"
    )
    use_ethiopic_job = fields.Boolean(
        config_parameter="l10n_et_hr.use_ethiopic_department_name"
    )
