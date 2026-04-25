# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import uuid

from openupgradelib import openupgrade

from odoo import Command

_deleted_xml_records = [
    "hr_attendance.hr_attendance_report_rule_multi_company",
    "hr_attendance.hr_attendance_rule_attendance_employee",
    "hr_attendance.hr_attendance_rule_attendance_manager",
    "hr_attendance.hr_attendance_rule_attendance_manual",
    "hr_attendance.hr_attendance_rule_attendance_overtime_employee",
    "hr_attendance.hr_attendance_rule_attendance_overtime_manager",
]


def fill_res_company_hr_attendance_display_overtime(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE res_company
        SET hr_attendance_display_overtime = hr_attendance_overtime
        """,
    )


def fill_res_company_attendance_kiosk_use_pin(env):
    group = env.ref("hr_attendance.group_hr_attendance_use_pin")
    openupgrade.logged_query(
        env.cr,
        f"""
        UPDATE res_company rc
        SET attendance_kiosk_use_pin = TRUE
        FROM res_users ru
        JOIN res_groups_users_rel group_rel ON group_rel.uid = ru.id
            AND group_rel.gid = {group.id}
        JOIN res_company_users_rel company_rel ON company_rel.user_id = ru.id
        WHERE company_rel.cid = rc.id AND ru.active
        """,
    )


def fill_res_company_attendance_kiosk_key(env):
    companies = env["res.company"].search([])
    for company in companies:
        company.attendance_kiosk_key = uuid.uuid4().hex


def fill_hr_attendance_overtime_hours(env):
    attendances = env["hr.attendance"].search([])
    # this way, the query in the compute method only is executed once
    attendances._compute_overtime_hours()


def hr_attendance_menus(env):
    group_hr_attendance = env.ref("hr_attendance.group_hr_attendance")
    group_hr_attendance_kiosk = env.ref("hr_attendance.group_hr_attendance_kiosk")
    # Remove the groups of 16.0 from the Attendances menu
    env.ref("hr_attendance.menu_hr_attendance_root").write(
        {
            "groups_id": [
                Command.unlink(group_hr_attendance.id),
                Command.unlink(group_hr_attendance_kiosk.id),
            ]
        }
    )
    openupgrade.rename_xmlids(
        env.cr,
        [
            (
                "hr_attendance.group_hr_attendance",
                "hr_attendance.group_hr_attendance_own_reader",
            ),
        ],
        allow_merge=True,
    )
    # Remove the groups of 16.0 from the Attendances > Kiosk Mode menu
    env.ref("hr_attendance.menu_hr_attendance_kiosk_no_user_mode").write(
        {
            "groups_id": [
                Command.unlink(group_hr_attendance_kiosk.id),
            ]
        }
    )
    openupgrade.rename_xmlids(
        env.cr,
        [
            (
                "hr_attendance.group_hr_attendance_kiosk",
                "hr_attendance.group_hr_attendance_own_reader",
            ),
        ],
        allow_merge=True,
    )


@openupgrade.migrate()
def migrate(env, version):
    fill_res_company_hr_attendance_display_overtime(env)
    fill_res_company_attendance_kiosk_use_pin(env)
    fill_res_company_attendance_kiosk_key(env)
    openupgrade.delete_records_safely_by_xml_id(env, _deleted_xml_records)
    fill_hr_attendance_overtime_hours(env)
    hr_attendance_menus(env)
