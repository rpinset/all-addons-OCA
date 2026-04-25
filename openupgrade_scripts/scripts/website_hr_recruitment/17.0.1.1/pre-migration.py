# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def _add_hr_job_published_date(env):
    openupgrade.add_fields(
        env,
        [
            (
                "published_date",
                "hr.job",
                "hr_job",
                "date",
                False,
                "website_hr_recruitment",
            )
        ],
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE hr_job
        SET published_date = CURRENT_DATE
        WHERE is_published;
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    _add_hr_job_published_date(env)
