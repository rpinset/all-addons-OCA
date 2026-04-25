from openupgradelib import openupgrade

xmlid_renames = [
    (
        "website_event.action_event_registration_report",
        "event.action_event_registration_report",
    ),
    (
        "website_event.access_event_question_answer_employee",
        "event.access_event_question_answer_employee",
    ),
    (
        "website_event.access_event_question_answer_registration",
        "event.access_event_question_answer_registration",
    ),
    (
        "website_event.access_event_question_answer_user",
        "event.access_event_question_answer_user",
    ),
    (
        "website_event.access_event_registration_answer",
        "event.access_event_registration_answer",
    ),
    (
        "website_event.constraint_event_registration_answer_value_check",
        "event.constraint_event_registration_answer_value_check",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(env.cr, "event_event", "location_menu"):
        # website_event was installed
        openupgrade.rename_xmlids(env.cr, xmlid_renames)
