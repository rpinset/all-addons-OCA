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


class HrApplicant(models.Model):

    _name = "hr.applicant"
    _inherit = "hr.applicant"

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

    ethiopic_name = fields.Char()
    use_ethiopic_dob = fields.Boolean("Use Ethiopic Birthday")
    etcal_dob_month = fields.Selection(ET_MONTHS_SELECTION, "Month")
    etcal_dob_day = fields.Selection(ET_DAYOFMONTH_SELECTION, "Day")
    etcal_dob_year = fields.Selection(_get_year, "Year")
    education = fields.Selection(
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

    @api.onchange("etcal_dob_day", "etcal_dob_month", "etcal_dob_year")
    def onchange_etdob(self):

        res = {"value": {"birth_date": False}}
        if self.etcal_dob_day and self.etcal_dob_month and self.etcal_dob_year:
            dob = pcc.gregorian_from_fixed(
                pcc.fixed_from_ethiopic(
                    pcc.ethiopic_date(
                        int(self.etcal_dob_year),
                        int(self.etcal_dob_month),
                        int(self.etcal_dob_day),
                    )
                )
            )
            res["value"]["birth_date"] = fields.Date.to_string(
                date(year=dob[0], month=dob[1], day=dob[2])
            )
        return res

    def create_employee_from_applicant(self):

        res = super().create_employee_from_applicant()

        for applicant in self:
            vals = {
                "default_certificate": applicant.education,
                "default_ethiopic_name": applicant.ethiopic_name,
                "default_use_ethiopic_dob": applicant.use_ethiopic_dob,
                "default_etcal_dob_year": applicant.etcal_dob_year,
                "default_etcal_dob_month": applicant.etcal_dob_month,
                "default_etcal_dob_day": applicant.etcal_dob_day,
            }
            res["context"].update(vals)

        return res
