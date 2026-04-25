# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.add_columns(env, [(False, "legal_name", "char", None, "hr_employee")])
    openupgrade.logged_query(
        env.cr, "UPDATE hr_employee SET legal_name = name WHERE legal_name IS NULL"
    )
