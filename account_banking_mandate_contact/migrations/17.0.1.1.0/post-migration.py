# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not openupgrade.column_exists(
        env.cr, "res_partner", "old_contact_mandate_17_id"
    ):
        return  # Already migrated in 16
    openupgrade.convert_to_company_dependent(
        env, "res.partner", "old_contact_mandate_17_id", "contact_mandate_id"
    )
