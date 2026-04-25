# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE iap_account
        SET name = service_name
        WHERE COALESCE(name, '') != ''
        """,
    )
    openupgrade.rename_columns(env.cr, {"iap_account": [("service_name", None)]})
