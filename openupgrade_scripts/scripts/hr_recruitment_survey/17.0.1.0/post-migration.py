# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def _hr_applicant_convert_response_ids_m2o_to_o2m(env):
    """
    Convert m2o to o2m in 'hr.applicant'
    """
    openupgrade.m2o_to_x2m(
        env.cr, env["hr.applicant"], "hr_applicant", "response_ids", "response_id"
    )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "hr_recruitment_survey", "17.0.1.0/noupdate_changes.xml")
    openupgrade.delete_record_translations(
        env.cr,
        "hr_recruitment_survey",
        ["group_hr_recruitment_interviewer"],
        ["comment"],
    )
    _hr_applicant_convert_response_ids_m2o_to_o2m(env)
