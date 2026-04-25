# Copyright 2024 Viindoo Technology Joint Stock Company (Viindoo)
# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

from dateutil.rrule import FR, MO, MONTHLY, SA, SU, TH, TU, WE, YEARLY, rrule
from openupgradelib import openupgrade

_deleted_xml_records = [
    "project.ir_cron_recurring_tasks",
    "project.mt_project_task_blocked",
    "project.mt_project_task_dependency_change",
    "project.mt_project_task_ready",
    "project.mt_task_blocked",
    "project.mt_task_dependency_change",
    "project.mt_task_progress",
    "project.mt_task_ready",
]


def _fill_project_task_display_in_project(env):
    """Set it to False when there's a parent but not display project."""
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE project_task
        SET display_in_project = False
        WHERE parent_id IS NOT NULL AND display_project_id IS NULL;
        """,
    )


def _convert_project_task_repeat_type_after(env):
    """Convert the disappeared "repeat N times" strategy to "repeat until"."""
    DAYS_MAPPING = {
        "mon": MO,
        "tue": TU,
        "wed": WE,
        "thu": TH,
        "fri": FR,
        "sat": SA,
        "sun": SU,
    }
    WEEKS_MAPPING = {"first": 1, "second": 2, "third": 3, "last": 4}
    MONTH_MAPPING = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12,
    }
    # First, expire all the already consumed recurrences
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE project_task_recurrence
        SET repeat_type = 'until',
            repeat_until = (CURRENT_DATE - interval '1 days')::date
        WHERE repeat_type = 'after'
            AND recurrence_left <= 0
        """,
    )
    # For day interval, we can do it massively by SQL, as there's no variability
    openupgrade.logged_query(
        env.cr,
        """
        WITH sub AS (
            SELECT recurrence_id, MAX(date_deadline) AS date_deadline
            FROM project_task
            WHERE recurrence_id IS NOT NULL
            GROUP by recurrence_id
        )
        UPDATE project_task_recurrence ptr
        SET repeat_type = 'until',
            repeat_until = (
                sub.date_deadline + (
                    interval '1 days' * ptr.repeat_interval * ptr.recurrence_left
                )
            )::date
        FROM sub
        WHERE ptr.id = sub.recurrence_id
            AND ptr.repeat_type = 'after'
            AND ptr.repeat_unit = 'day'
            AND ptr.recurrence_left > 0
        """,
    )
    # WEEK
    # - Obtain the number of days per week of each ocurrence
    # - Get the remaining weeks from the number of days per week
    # - Always put the end date on the last day of the week (Sunday)
    env.cr.execute(
        """
        SELECT
            ptr.id, ptr.recurrence_left, ptr.repeat_interval,
            ptr.mon, ptr.tue, ptr.wed, ptr.thu, ptr.fri, ptr.sat, ptr.sun,
            MAX(pt.date_deadline) AS date_deadline
        FROM project_task pt JOIN project_task_recurrence ptr
            ON ptr.id = pt.recurrence_id
        WHERE ptr.repeat_type = 'after'
            AND ptr.repeat_unit = 'week'
            AND date_deadline IS NOT NULL
        GROUP BY pt.id, ptr.id
        """
    )
    for row in env.cr.dictfetchall():
        ptr = env["project.task.recurrence"].browse(row["id"])
        days_per_week = sum(1 if row[x] else 0 for x in DAYS_MAPPING)
        weeks = int(row["recurrence_left"] % days_per_week) + 1
        repeat_until = row["date_deadline"] + timedelta(
            weeks=weeks * row["repeat_interval"]
        )
        repeat_until += timedelta(days=6 - repeat_until.weekday())  # Put Sunday
        ptr.write({"repeat_type": "until", "repeat_until": repeat_until})
    # MONTH AND YEAR
    # - Build rrule inspired on v16 code, but in an optimized way
    # - Get end date through rrule execution
    env.cr.execute(
        """
        SELECT
            ptr.id, ptr.recurrence_left, ptr.repeat_interval, ptr.repeat_unit,
            ptr.repeat_on_month, ptr.repeat_on_year, ptr.repeat_day, ptr.repeat_month,
            ptr.repeat_week, ptr.repeat_weekday, MAX(pt.date_deadline) AS date_deadline
        FROM project_task pt JOIN project_task_recurrence ptr
            ON ptr.id = pt.recurrence_id
        WHERE ptr.repeat_type = 'after'
            AND ptr.repeat_unit IN ('month', 'year')
            AND date_deadline IS NOT NULL
        GROUP BY pt.id, ptr.id
        """
    )
    for row in env.cr.dictfetchall():
        ptr = env["project.task.recurrence"].browse(row["id"])
        rrule_kwargs = {
            "interval": row["recurrence_left"] * row["repeat_interval"],
            "dtstart": row["date_deadline"],
            "freq": MONTHLY if row["repeat_unit"] == "month" else YEARLY,
        }
        if (row["repeat_on_month"] == "day" and row["repeat_unit"] == "month") or (
            row["repeat_on_year"] == "day" and row["repeat_unit"] == "year"
        ):
            rrule_kwargs["byweekday"] = [
                DAYS_MAPPING[row["repeat_weekday"]](WEEKS_MAPPING[row["repeat_week"]])
            ]
        if row["repeat_unit"] == "year" and row["repeat_on_year"] == "date":
            rrule_kwargs["bymonth"] = MONTH_MAPPING[row["repeat_month"]]
        repeat_until = list(rrule(**rrule_kwargs))[1]
        if row["repeat_unit"] == "month" and row["repeat_on_month"] == "date":
            repeat_until = repeat_until.replace(day=int(row["repeat_day"]))
        if row["repeat_unit"] == "year" and row["repeat_on_year"] == "date":
            repeat_until = repeat_until.replace(
                day=int(row["repeat_day"]), month=MONTH_MAPPING[row["repeat_month"]]
            )
        ptr.write({"repeat_type": "until", "repeat_until": repeat_until})


def _fill_project_update_task_count(env):
    """Use an heuristics to get the fields task_count and closed_task_count for
    historical project updates:

    - Task count: the number of tasks which creation date is below project update
      creation date.
    - Closed task count: the number of tasks which end date is below project update
      creation date.
    """
    for update in env["project.update"].search([]):
        base_domain = [("display_project_id", "=", update.project_id.id)]
        update.task_count = env["project.task"].search_count(
            base_domain + [("create_date", "<=", update.create_date)]
        )
        update.closed_task_count = env["project.task"].search_count(
            base_domain + [("date_end", "<=", update.create_date)]
        )


@openupgrade.migrate()
def migrate(env, version):
    _fill_project_task_display_in_project(env)
    _convert_project_task_repeat_type_after(env)
    openupgrade.load_data(env, "project", "17.0.1.3/noupdate_changes.xml")
    openupgrade.delete_record_translations(
        env.cr,
        "project",
        ("project_message_user_assigned", "rating_project_request_email_template"),
    )
    openupgrade.delete_records_safely_by_xml_id(
        env,
        _deleted_xml_records,
    )
