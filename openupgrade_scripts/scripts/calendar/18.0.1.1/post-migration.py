# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "calendar", "18.0.1.1/noupdate_changes.xml")
    openupgrade.delete_record_translations(
        env.cr,
        "calendar",
        [
            "calendar_template_meeting_changedate",
            "calendar_template_meeting_invitation",
            "calendar_template_meeting_reminder",
            "calendar_template_meeting_update",
        ],
    )
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "calendar.onboarding_onboarding_calendar",
            "calendar.onboarding_onboarding_step_setup_calendar_integration",
        ],
    )
