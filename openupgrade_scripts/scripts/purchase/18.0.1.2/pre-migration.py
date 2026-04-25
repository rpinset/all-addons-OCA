# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def fill_purchase_order_amount_total_cc(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE purchase_order
        SET amount_total_cc = amount_total / currency_rate
        WHERE COALESCE(currency_rate, 0) != 0""",
    )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.delete_sql_constraint_safely(
        env, "purchase", "purchase_order_line", "accountable_required_fields"
    )
    openupgrade.add_columns(
        env, [("purchase.order", "amount_total_cc", "float", None, "purchase_order")]
    )
    fill_purchase_order_amount_total_cc(env)
