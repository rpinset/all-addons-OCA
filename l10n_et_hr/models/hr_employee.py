# Copyright (C) 2022 Trevi Software (https://trevi.et)
# Copyright (C) 2013 Michael Telahun Makonnen <mmakonnen@gmail.com>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime

from odoo import api, fields, models

from odoo.addons.ethiopic_calendar.models.ethiopic_calendar import (
    ET_DAYOFMONTH_SELECTION,
    ET_MONTHS_SELECTION,
)
from odoo.addons.ethiopic_calendar.models.pycalcal import pycalcal as pcc


class HrEmployee(models.Model):

    _inherit = "hr.employee"

    @api.model
    def _get_year(self):

        res = []

        # Assuming employees are at least 16 years old
        year = datetime.now().year
        year -= 16

        # Convert to Ethiopic calendar
        pccDate = pcc.ethiopic_from_fixed(
            pcc.fixed_from_gregorian(pcc.gregorian_date(year, 1, 1))
        )
        year = pccDate[0]

        i = year
        while i > (year - 59):
            res.append((str(i), str(i)))
            i -= 1

        return res

    certificate = fields.Selection(
        selection_add=[
            ("none", "No Formal Education"),
            ("primary", "Primary School"),
            ("graduate", "Secondary School"),
            ("diploma", "Diploma"),
            ("bachelor",),
            ("master",),
            ("doctor",),
            ("other",),
        ],
    )
    ethiopic_name = fields.Char()
    use_ethiopic_dob = fields.Boolean("Use Ethiopic Birthday")
    etcal_dob_month = fields.Selection(
        ET_MONTHS_SELECTION, "Month", groups="hr.group_hr_user", tracking=True
    )
    etcal_dob_day = fields.Selection(
        ET_DAYOFMONTH_SELECTION, "Day", groups="hr.group_hr_user", tracking=True
    )
    etcal_dob_year = fields.Selection(
        _get_year, "Year", groups="hr.group_hr_user", tracking=True
    )

    @api.onchange("etcal_dob_day", "etcal_dob_month", "etcal_dob_year")
    def onchange_etdob(self):

        for rec in self:
            if rec.etcal_dob_day and rec.etcal_dob_month and rec.etcal_dob_year:
                dob = pcc.gregorian_from_fixed(
                    pcc.fixed_from_ethiopic(
                        pcc.ethiopic_date(
                            int(rec.etcal_dob_year),
                            int(rec.etcal_dob_month),
                            int(rec.etcal_dob_day),
                        )
                    )
                )
                rec.birthday = fields.Date.to_string(
                    date(year=dob[0], month=dob[1], day=dob[2])
                )
            else:
                rec.birthday = False
