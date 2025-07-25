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


class NewLabour(models.TransientModel):

    _inherit = "hr.employee.wizard.new"

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

    # Personal Details
    #
    ethiopic_name = fields.Char(size=512)
    use_ethiopic_dob = fields.Boolean(string="Use Ethiopic Birthday", default=True)
    etcal_dob_month = fields.Selection(selection=ET_MONTHS_SELECTION, string="Month")
    etcal_dob_day = fields.Selection(selection=ET_DAYOFMONTH_SELECTION, string="Day")
    etcal_dob_year = fields.Selection(selection=_get_year, string="Year")
    house_no = fields.Char(string="House No.")
    kebele = fields.Char(size=8)
    woreda = fields.Char(string="Subcity/Woreda")
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

    @api.onchange("etcal_dob_month", "etcal_dob_day", "etcal_dob_year")
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

    def create_partner(self):

        res = super().create_partner()
        for rec in self:
            hno = rec.house_no and ("House No: " + rec.house_no) or ""
            kebele = rec.kebele and ("Kebele: " + rec.kebele) or ""
            woreda = rec.woreda and ("Subcity/Woreda: " + rec.woreda) or ""
            partner_vals = {
                "street": woreda + " " + kebele + " " + hno,
            }
            rec.write(partner_vals)

        return res

    def _create_hr_applicant(self, partner):

        res = super()._create_hr_applicant(partner)
        applicant_vals = {
            "education": self.education,
            "ethiopic_name": self.ethiopic_name,
            "use_ethiopic_dob": self.use_ethiopic_dob,
            "etcal_dob_year": self.use_ethiopic_dob and self.etcal_dob_year or False,
            "etcal_dob_month": self.use_ethiopic_dob and self.etcal_dob_month or False,
            "etcal_dob_day": self.use_ethiopic_dob and self.etcal_dob_day or False,
        }
        res.write(applicant_vals)
        return res

    def _get_employee_values(self, context):

        res = super()._get_employee_values(context)
        res.update(
            {
                "ethiopic_name": context["default_ethiopic_name"],
                "use_ethiopic_dob": context["default_use_ethiopic_dob"],
                "etcal_dob_year": context["default_etcal_dob_year"],
                "etcal_dob_month": context["default_etcal_dob_month"],
                "etcal_dob_day": context["default_etcal_dob_day"],
                "certificate": context["default_certificate"],
            }
        )
        return res
