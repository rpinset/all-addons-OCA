# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade

_columns_copy = {
    "stock_move": [("location_dest_id", None, None)],
}

_field_renames = [
    ("stock.move", "stock_move", "location_dest_id", "location_final_id"),
    (
        "stock.warehouse.orderpoint",
        "stock_warehouse_orderpoint",
        "qty_to_order",
        "qty_to_order_manual",
    ),
]

_xmlid_renames = [
    ("stock.stock_location_inter_wh", "stock.stock_location_inter_company"),
]

_new_columns = [
    ("product.template", "is_storable", "boolean", False),
    ("stock.move", "location_dest_id", "many2one"),
    ("stock.rule", "location_dest_from_rule", "boolean", False),
    ("stock.picking.type", "move_type", "selection", "direct"),
    ("stock.putaway.rule", "sublocation", "selection", "no"),
]


def fill_product_template_is_storable(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE product_template
        SET is_storable = TRUE, type = 'consu'
        WHERE type = 'product'""",
    )


def fill_stock_move_location_dest_id(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE stock_move sm2
        SET location_dest_id = COALESCE(sp.location_dest_id,
            spt.default_location_dest_id, sm.location_final_id)
        FROM stock_move sm
        LEFT JOIN stock_picking sp ON sm.picking_id = sp.id
        LEFT JOIN stock_picking_type spt ON sm.picking_type_id = spt.id
        WHERE sm2.id = sm.id
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        WITH RECURSIVE sub AS (
            (SELECT rel.move_orig_id, rel.move_dest_id
            FROM stock_move_move_rel rel
            LEFT JOIN stock_move_move_rel rel2 ON rel.move_dest_id = rel2.move_orig_id
            WHERE rel2.move_orig_id IS NULL)
            UNION
            (SELECT rel.move_orig_id, sub.move_dest_id
            FROM stock_move_move_rel rel
            JOIN sub ON sub.move_orig_id = rel.move_dest_id)
        )
        UPDATE stock_move sm2
        SET location_final_id = sm.location_final_id
        FROM stock_rule sr, stock_move sm
        JOIN sub ON sub.move_dest_id = sm.id
        WHERE sm2.rule_id = sr.id AND sub.move_orig_id = sm2.id
            AND sr.action IN ('push', 'pull_push')
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        WITH sub AS (
            UPDATE stock_move sm
            SET location_final_id = sr.location_dest_id
            FROM stock_rule sr
            WHERE sm.rule_id = sr.id AND sr.location_dest_id IS NOT NULL
                AND sr.location_dest_id != sm.location_final_id
                AND sr.location_dest_id != sm.location_dest_id
                AND sr.action IN ('pull', 'pull_push')
            RETURNING rule_id
        ), sub2 AS (
            SELECT rule_id
            FROM sub
            GROUP BY rule_id
        )
        UPDATE stock_rule sr
        SET location_dest_from_rule = TRUE
        FROM sub2
        WHERE sub2.rule_id = sr.id
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        WITH sub AS (
            SELECT sm.rule_id
            FROM stock_move sm
            JOIN stock_move_move_rel rel ON
                rel.move_orig_id = sm.id OR rel.move_dest_id = sm.id
            JOIN stock_rule sr ON sm.rule_id = sr.id
            WHERE sr.action IN ('pull', 'pull_push')
            GROUP BY sm.rule_id
        )
        UPDATE stock_rule sr
        SET location_dest_from_rule = TRUE
        FROM sub
        WHERE sub.rule_id = sr.id
        """,
    )


def fill_stock_putaway_rule_sublocation(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE stock_putaway_rule
        SET sublocation = 'closest_location'
        WHERE storage_category_id is not null""",
    )


@openupgrade.migrate()
def migrate(env, version=None):
    if openupgrade.column_exists(env.cr, "product_template", "responsible_id"):
        # in v12, this field was not company_dependent
        openupgrade.rename_columns(
            env.cr,
            {"product_template": [("responsible_id", None)]},
        )
    openupgrade.copy_columns(env.cr, _columns_copy)
    openupgrade.rename_fields(env, _field_renames)
    openupgrade.rename_xmlids(env.cr, _xmlid_renames)
    openupgrade.add_columns(env, _new_columns)
    fill_product_template_is_storable(env)
    fill_stock_move_location_dest_id(env)
    fill_stock_putaway_rule_sublocation(env)
