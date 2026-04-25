from openupgradelib import openupgrade

_new_columns = [
    (
        "hr.employee",
        "distance_home_work_unit",
        "selection",
        "kilometers",
        "hr_employee",
    ),
    ("hr.employee", "is_flexible", "boolean", None, "hr_employee"),
    ("hr.employee", "is_fully_flexible", "boolean", None, "hr_employee"),
    ("res.company", "hr_presence_control_attendance", "boolean"),
    ("res.company", "hr_presence_control_email", "boolean"),
    ("res.company", "hr_presence_control_ip", "boolean"),
    ("res.company", "hr_presence_control_login", "boolean", True),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_columns(
        env.cr, {"employee_category_rel": [("emp_id", "employee_id")]}
    )
    openupgrade.add_columns(env, _new_columns)
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE hr_employee
        SET is_fully_flexible = CASE WHEN resource_calendar_id IS NULL
                                     THEN TRUE ELSE FALSE END
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE hr_employee he2
        SET is_flexible = CASE WHEN he.is_fully_flexible OR rc.flexible_hours
                               THEN TRUE ELSE FALSE END
        FROM hr_employee he
        LEFT JOIN resource_calendar rc ON he.resource_calendar_id = rc.id
        WHERE he.id = he2.id
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE hr_employee
        SET marital = 'single'
        WHERE marital IS NULL
        """,
    )
