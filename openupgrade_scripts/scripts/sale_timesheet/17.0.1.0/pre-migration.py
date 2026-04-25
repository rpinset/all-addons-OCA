# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def _fill_project_project_billing_type(env):
    """Field `billing_type` on project.project is a new stored field."""
    openupgrade.add_fields(
        env,
        [
            (
                "billing_type",
                "project.project",
                "project_project",
                "selection",
                False,
                "sale_timesheet",
                "not_billable",
            )
        ],
    )


@openupgrade.migrate()
def migrate(env, version):
    _fill_project_project_billing_type(env)
