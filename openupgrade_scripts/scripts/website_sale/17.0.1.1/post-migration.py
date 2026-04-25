# Copyright 2025 Tecnativa - Pilar Vargas
# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def _adjust_website_default_b2b_b2c(env):
    """Previously, B2B/B2C prices visibility was set in a global way through 2
    accounting groups that were inherited to "Internal user" group. Now, these groups
    have disappeared, and this can be configured at website level directly. We switch
    from the default value "tax_excluded" if we detect the B2C group was put before.
    This can be done because the groups haven't been yet removed in this phase.
    """
    group_b2c = env.ref("account.group_show_line_subtotals_tax_included")
    group_internal = env.ref("base.group_user")
    if group_b2c in group_internal.implied_ids:
        env["website"].search([]).show_line_subtotals_tax_selection = "tax_included"


@openupgrade.migrate()
def migrate(env, version):
    # Set to False so as not to change the behaviour of the website with new things.
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE product_tag SET visible_on_ecommerce = FALSE
        WHERE visible_on_ecommerce IS DISTINCT FROM FALSE
        """,
    )
    if openupgrade.column_exists(env.cr, "ir_attachment", "product_downloadable"):
        # due to website_sale_digital
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE product_document
            SET attached_on = 'sale_order'
            FROM ir_attachment ir
            WHERE product_document.ir_attachment_id = ir.id
              AND ir.product_downloadable
            """,
        )
    _adjust_website_default_b2b_b2c(env)
