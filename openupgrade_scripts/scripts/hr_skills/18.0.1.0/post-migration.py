# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.convert_field_to_html(
        env.cr,
        "hr_resume_line",
        openupgrade.get_legacy_name("description"),
        "description",
        verbose=False,
        translate=True,
    )
