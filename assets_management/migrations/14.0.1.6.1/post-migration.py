# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    mode_line = env.ref(
        "assets_management.ad_mode_materiale_line",
        raise_if_not_found=False,
    )
    if mode_line and not mode_line.from_year_nr and not mode_line.to_year_nr:
        openupgrade.load_data(
            env.cr,
            "assets_management",
            "migrations/14.0.1.6.1/noupdate_changes.xml",
        )
