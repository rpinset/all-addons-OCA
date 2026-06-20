# Copyright (C) 2025 Trevi Software (https://trevi.et)
# Copyright (C) 2013 Michael Telahun Makonnen <mmakonnen@gmail.com>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from datetime import datetime
from pytz import timezone, UTC

from odoo import api, fields, models
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT as OE_DTFORMAT
from odoo.tools.translate import _

from odoo.addons.ethiopic_calendar.models.ethiopic_calendar import (
    ET_MONTHS_SELECTION_AM,
)
from odoo.addons.ethiopic_calendar.models.pycalcal import pycalcal as pcc


_logger = logging.getLogger(__name__)
class HrLeave(models.Model):

    _inherit = "hr.leave"

    return_date_et = fields.Char("Ethiopic Return Date")

    local_date_from = fields.Datetime("Local Date From", compute="_localize_date_from_to")

    local_date_to = fields.Datetime("Local Date To", compute="_localize_date_from_to")

    rest_days = fields.Float(
        "Rest (Days)",
        compute="_compute_rest_days",
        store=True,
        readonly=False,
        copy=False,
        tracking=True,
        help="Number of rest days of the time off request",
    )

    public_holiday_days = fields.Float(
        "Public Holiday (Days)",
        compute="_compute_public_holiday_days",
        store=True,
        readonly=False,
        copy=False,
        tracking=True,
        help="Number of public holidays in the time off request",
    )

    real_days = fields.Float(
        "Real (Days)",
        compute="_compute_real_days",
        store=True,
        readonly=False,
        copy=False,
        tracking=True,
        help="Number of actual days, including holidays and days off, "
        "in the time off request",
    )

    available_leave_days = fields.Float(
        "Available Leave Days",
        compute="_compute_available_leave_days",
        readonly=True,
        tracking=False,
        help="Number of available leave days for the employee",)

    taken_leave_days = fields.Float(
        "Taken Leave Days",
        compute="_compute_taken_leave_days",
        readonly=True,
        tracking=False,
        help="Number of available leave days for the employee",)

    def _compute_rest_days(self):
        for record in self:
            record.rest_days = 0

    def _compute_public_holiday_days(self):
        for record in self:
            public_holidays = self.env["hr.holidays.public.line"].search(
                [
                    ("date", ">=", record.date_from),
                    ("date", "<", record.date_to),
                ]
            )
            record.public_holiday_days = len(public_holidays)

    @api.depends("number_of_days", "rest_days", "public_holiday_days")
    def _compute_real_days(self):
        for record in self:
            record.real_days = (
                record.number_of_days + record.rest_days + record.public_holiday_days
            )

    @api.depends("number_of_days")
    def _compute_taken_leave_days(self):
        leaves = self.env["hr.leave"]
        for record in self:
            taken_leaves = leaves.search([
                ("employee_id", "=", record.employee_id.id),
                ("holiday_status_id", "=", record.holiday_status_id.id),
                ("state", "=", "validate"),
            ])
            record.taken_leave_days = sum(taken_leaves.mapped("number_of_days"))

    @api.depends("number_of_days", "taken_leave_days")
    def _compute_available_leave_days(self):
        allocation = self.env["hr.leave.allocation"]
        for record in self:
            my_allocations = allocation.search([
                ("employee_id", "=", record.employee_id.id),
                ("holiday_status_id", "=", record.holiday_status_id.id),
                ("state", "=", "validate"),
            ])
            record.available_leave_days = (
                sum(my_allocations.mapped("number_of_days")) - record.taken_leave_days
            )

    @api.model
    def time2ethiopic(self, year, month, day):

        # Convert to Ethiopic calendar
        pcc_date = pcc.ethiopic_from_fixed(
            pcc.fixed_from_gregorian(pcc.gregorian_date(year, month, day))
        )

        return (
            ""
            + ET_MONTHS_SELECTION_AM[pcc_date[1] - 1][1]
            + " "
            + str(pcc_date[2])
            + ", "
            + str(pcc_date[0])
        )

    @api.onchange("date_to")
    def onchange_enddate(self):

        for record in self:
            dt = record.date_to
            if record.date_to:
                record.return_date_et = record.time2ethiopic(
                        int(dt.strftime("%Y")),
                        int(dt.strftime("%m")),
                        int(dt.strftime("%d")),
                    )

    @api.model
    def format_date(self, date_str):

        if not date_str:
            return ""
        d = datetime.strptime(date_str, OE_DTFORMAT)
        return d.strftime("%b %d, %Y")

    @api.model
    def format_date_et(self, date_str):

        if not date_str:
            return ""
        d = datetime.strptime(date_str, OE_DTFORMAT)
        return self.env["hr.leave"].time2ethiopic(d.year, d.month, d.day)

    @api.model
    def get_remaining_leaves(self, leave):

        obj = self.env["hr.leave.type"]
        res = obj.get_remaining_days_by_employee(
            [leave.holiday_status_id.id], leave.employee_id.id
        )
        res = res[leave.employee_id.id]
        if (
            res[leave.holiday_status_id.id].get("max_leaves", False)
            and res[leave.holiday_status_id.id]["max_leaves"] > 0
        ):
            days = res[leave.holiday_status_id.id]["remaining_leaves"]
            if leave.state not in ["validate", "validate1"]:
                days = (
                    res[leave.holiday_status_id.id]["remaining_leaves"]
                    - leave.number_of_days_temp
                )
        else:
            days = ""

        return days

    @api.model
    def get_taken_leaves(self, leave):

        obj = self.env["hr.leave.type"]
        res = obj.get_remaining_days_by_employee(
            [leave.holiday_status_id.id], leave.employee_id.id
        )
        res = res[leave.employee_id.id]
        if (
            res[leave.holiday_status_id.id].get("max_leaves", False)
            and res[leave.holiday_status_id.id]["max_leaves"] > 0
        ):
            days = (
                res[leave.holiday_status_id.id]["max_leaves"]
                - res[leave.holiday_status_id.id]["remaining_leaves"]
            )

            # We only want leaves taken so far, *EXCLUDING* this one
            if leave.state in ["validate", "validate1"]:
                days -= leave.number_of_days_temp
        else:
            days = ""

        return days

    @api.model
    def get_hrm(self):

        hrm_data = ("", "", _("HR Manager"), "የሠው ሃይል አስተዳደር")
        hrm_dict = self.env["hr.config.settings"].get_default_hr_manager_id(False)
        hrm_id = hrm_dict["hr_manager_id"]
        if hrm_id:
            hrm = self.env["hr.employee"].browse(hrm_id)
            hrm_data = (
                hrm.name,
                hrm.ethiopic_name,
                hrm.contract_id.job_id.name,
                hrm.contract_id.job_id.ethiopic_name,
            )

        return hrm_data

    @api.depends('date_from', 'date_to')
    def _localize_date_from_to(self):

        for record in self:
            if record.date_from:
                record.local_date_from = UTC \
                                            .localize(record.date_from) \
                                            .astimezone(timezone(
                                                record.employee_id.tz or 'UTC'
                                            )) \
                                            .replace(tzinfo=None)
                
            else:
                record.local_date_from = False
            if record.date_to:
                record.local_date_to = UTC \
                                            .localize(record.date_to) \
                                            .astimezone(timezone(
                                                record.employee_id.tz or 'UTC'
                                            )) \
                                            .replace(tzinfo=None)
            else:
                record.local_date_to = False
