# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        "UPDATE res_partner SET peppol_eas = NULL "
        "WHERE peppol_eas IN ('0212', '0215', '9901')",
    )
