# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    group_holidays_user = env.ref("hr_holidays.group_hr_holidays_user", False)
    # In v17 the group_hr_attendance_user was renamed to group_hr_attendance_officer
    # so, we need to remove this group from the implied_ids
    # see https://github.com/odoo/odoo/commit/bf67f1e20e0bc0cfc48f32114383f36fa0b09dfe
    group_hr_attendance = env.ref("hr_attendance.group_hr_attendance_officer", False)
    if group_holidays_user and group_hr_attendance:
        group_holidays_user.write({"implied_ids": [(3, group_hr_attendance.id)]})
