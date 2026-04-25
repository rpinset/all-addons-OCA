from openupgradelib import openupgrade

_xmlids_renames = [
    (
        "delivery.act_delivery_trackers_url",
        "stock_delivery.act_delivery_trackers_url",
    ),
    (
        "delivery.access_choose_delivery_package",
        "stock_delivery.access_choose_delivery_package",
    ),
    (
        "delivery.access_delivery_carrier_stock_user",
        "stock_delivery.access_delivery_carrier_stock_user",
    ),
    (
        "delivery.access_delivery_carrier_stock_manager",
        "stock_delivery.access_delivery_carrier_stock_manager",
    ),
    (
        "delivery.access_delivery_price_rule_stock_manager",
        "stock_delivery.access_delivery_price_rule_stock_manager",
    ),
    (
        "delivery.access_delivery_zip_prefix_stock_manager",
        "stock_delivery.access_delivery_zip_prefix_stock_manager",
    ),
    (
        "delivery.menu_action_delivery_carrier_form",
        "stock_delivery.menu_action_delivery_carrier_form",
    ),
    (
        "delivery.menu_delivery_zip_prefix",
        "stock_delivery.menu_delivery_zip_prefix",
    ),
    (
        "delivery.model_choose_delivery_package",
        "stock_delivery.model_choose_delivery_package",
    ),
    (
        "delivery.choose_delivery_package_view_form",
        "stock_delivery.choose_delivery_package_view_form",
    ),
    (
        "delivery.delivery_stock_report_delivery_no_package_section_line",
        "stock_delivery.delivery_stock_report_delivery_no_package_section_line",
    ),
    (
        "delivery.delivery_tracking_url_warning_form",
        "stock_delivery.delivery_tracking_url_warning_form",
    ),
    (
        "delivery.label_package_template_view_delivery",
        "stock_delivery.label_package_template_view_delivery",
    ),
    (
        "delivery.product_template_hs_code",
        "stock_delivery.product_template_hs_code",
    ),
    (
        "delivery.report_delivery_document2",
        "stock_delivery.report_delivery_document2",
    ),
    (
        "delivery.report_package_barcode_delivery",
        "stock_delivery.report_package_barcode_delivery",
    ),
    (
        "delivery.report_package_barcode_small_delivery",
        "stock_delivery.report_package_barcode_small_delivery",
    ),
    (
        "delivery.report_shipping2",
        "stock_delivery.report_shipping2",
    ),
    (
        "delivery.sale_order_portal_content_inherit_sale_stock_inherit_website_sale_delivery",
        "stock_delivery.sale_order_portal_content_inherit_sale_stock_inherit_website_sale",
    ),
    (
        "delivery.stock_move_line_view_search_delivery",
        "stock_delivery.stock_move_line_view_search_delivery",
    ),
    (
        "delivery.stock_package_type_form_delivery",
        "stock_delivery.stock_package_type_form_delivery",
    ),
    (
        "delivery.stock_package_type_tree_delivery",
        "stock_delivery.stock_package_type_tree_delivery",
    ),
    (
        "delivery.stock_report_delivery_aggregated_move_lines_inherit_delivery",
        "stock_delivery.stock_report_delivery_aggregated_move_lines_inherit_delivery",
    ),
    (
        "delivery.stock_report_delivery_has_serial_move_line_inherit_delivery",
        "stock_delivery.stock_report_delivery_has_serial_move_line_inherit_delivery",
    ),
    (
        "delivery.stock_report_delivery_package_section_line_inherit_delivery",
        "stock_delivery.stock_report_delivery_package_section_line_inherit_delivery",
    ),
    (
        "delivery.view_move_line_tree_detailed_delivery",
        "stock_delivery.view_move_line_tree_detailed_delivery",
    ),
    (
        "delivery.view_picking_type_form_delivery",
        "stock_delivery.view_picking_type_form_delivery",
    ),
    (
        "delivery.view_picking_withcarrier_out_form",
        "stock_delivery.view_picking_withcarrier_out_form",
    ),
    (
        "delivery.view_picking_withweight_internal_move_form",
        "stock_delivery.view_picking_withweight_internal_move_form",
    ),
    (
        "delivery.view_quant_package_weight_form",
        "stock_delivery.view_quant_package_weight_form",
    ),
    (
        "delivery.view_stock_rule_form_delivery",
        "stock_delivery.view_stock_rule_form_delivery",
    ),
    (
        "delivery.vpicktree_view_tree",
        "stock_delivery.vpicktree_view_tree",
    ),
]


def _delete_sql_constraints(env):
    # Delete constraints to recreate it
    openupgrade.delete_sql_constraint_safely(
        env, "delivery", "delivery_carrier", "margin_not_under_100_percent"
    )


def _fill_sale_order_shipping_weight(env):
    """Field `shipping_weight` on sale.order is a new stored field."""
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE sale_order
        ADD COLUMN IF NOT EXISTS shipping_weight float8;
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        WITH weight_data AS (
            SELECT
                SUM(
                    COALESCE(sol.product_uom_qty, 0) * COALESCE(p.weight, 0)
                ) AS shipping_weight,
                sol.order_id
            FROM sale_order_line sol
            JOIN product_product p ON sol.product_id = p.id
            JOIN product_template pt ON p.product_tmpl_id = pt.id
            WHERE pt.type IN ('product', 'consu')
                AND (sol.is_delivery IS NULL OR sol.is_delivery = FALSE)
                AND sol.display_type IS NULL
                AND sol.product_uom_qty > 0
            GROUP BY sol.order_id
        )
        UPDATE sale_order so
        SET shipping_weight = wd.shipping_weight
        FROM weight_data wd
        WHERE so.id = wd.order_id;
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """UPDATE sale_order
           SET shipping_weight = 0
           WHERE shipping_weight IS NULL
        """,
    )


def _fill_stock_move_line_carrier_id(env):
    """Field `carrier_id` on stock.move.line is now a stored field."""
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE stock_move_line
        ADD COLUMN IF NOT EXISTS carrier_id INTEGER;
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE stock_move_line sml
        SET carrier_id = sp.carrier_id
        FROM stock_picking sp
        WHERE sml.picking_id = sp.id;
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, _xmlids_renames)
    _delete_sql_constraints(env)
    _fill_sale_order_shipping_weight(env)
    _fill_stock_move_line_carrier_id(env)
    openupgrade.logged_query(  # just to be sure
        env.cr,
        """
        UPDATE ir_module_module
        SET state='to install'
        WHERE name = 'stock_delivery' AND state='uninstalled'""",
    )
