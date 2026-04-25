# Copyright 2024 Viindoo Technology Joint Stock Company (Viindoo)
# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def _project_update_fill_timesheet(env):
    """Fill existing project updates with the theoretical information about the number
    of allocated and spent hours. It may be different from the ones existing on the
    moment the project update was done if later modifications changed them.
    """
    uom_hour = env.ref("uom.product_uom_hour")
    for update in env["project.update"].with_context(active_test=False).search([]):
        project = update.project_id
        group = env["account.analytic.line"]._read_group(
            [("project_id", "=", project.id), ("date", "<=", update.date)],
            [],
            ["unit_amount:sum"],
        )[0]
        update.write(
            {
                "uom_id": uom_hour.id,
                "allocated_time": round(project.allocated_hours),
                "timesheet_time": round(group[0]),
            }
        )


@openupgrade.migrate()
def migrate(env, version):
    _project_update_fill_timesheet(env)
