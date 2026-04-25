# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        f"""
        UPDATE iap_account ia
        SET service_id = ise.id
        FROM iap_service ise
        WHERE ia.service_id IS NULL AND
            ise.technical_name = ia.{openupgrade.get_legacy_name("service_name")}
        """,
    )
    openupgrade.logged_query(
        env.cr,
        f"""
        DELETE FROM iap_account
        WHERE service_id IS NULL
            AND {openupgrade.get_legacy_name("service_name")} IS NOT NULL
        """,
    )
    env["iap.account"]._add_sql_constraints()
