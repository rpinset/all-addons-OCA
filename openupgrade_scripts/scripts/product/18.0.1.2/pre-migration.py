# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

xmlid_renames = [
    ("product.group_discount_per_so_line", "sale.group_discount_per_so_line"),
]

column_creates = [
    ("product.attribute", "active", "boolean", True),
    ("product.attribute.value", "active", "boolean", True),
    ("product.pricelist.item", "display_applied_on", "char"),
    ("product.pricelist.item", "price_markup", "float"),
]


def rename_pos_models(env):
    """
    pos.combo and pos.combo.line have been moved to product from point_of_sale and
    renamed to product.combo and product.combo.item respectively
    """
    if not openupgrade.table_exists(env.cr, "pos_combo"):
        return
    openupgrade.rename_tables(
        env.cr,
        [
            ("pos_combo", "product_combo"),
            ("pos_combo_line", "product_combo_item"),
            ("pos_combo_product_template_rel", "product_combo_product_template_rel"),
        ],
    )
    openupgrade.rename_columns(
        env.cr,
        {
            "product_combo_product_template_rel": [
                ("pos_combo_id", "product_combo_id"),
            ]
        },
    )
    openupgrade.rename_models(
        env.cr,
        [
            ("pos.combo", "product.combo"),
            ("pos.combo.line", "product.combo.item"),
        ],
    )
    openupgrade.rename_fields(
        env,
        [
            ("product.combo", "product_combo", "combo_line_ids", "combo_item_ids"),
            ("product.combo.item", "product_combo_item", "combo_price", "extra_price"),
        ],
    )


def fill_product_pricelist_item_columns(env):
    """
    Set display_applied_on to '2_product_category' if applied_on is
    '2_product_category', else '1_product'
    Set price_markup = -price_discount
    """
    env.cr.execute(
        """
        UPDATE product_pricelist_item
        SET
        display_applied_on=CASE
            WHEN applied_on='2_product_category' THEN '2_product_category'
            ELSE '1_product'
        END,
        price_markup=-price_discount
        """
    )


def assure_service_tracking(env):
    if not openupgrade.column_exists(env.cr, "product_template", "service_tracking"):
        return
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE product_template
        SET service_tracking = 'no'
        WHERE service_tracking IS NULL
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, xmlid_renames)
    openupgrade.add_columns(env, column_creates)
    fill_product_pricelist_item_columns(env)
    rename_pos_models(env)
    assure_service_tracking(env)
