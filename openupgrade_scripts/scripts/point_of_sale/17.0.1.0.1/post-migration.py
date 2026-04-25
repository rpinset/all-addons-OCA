# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def fill_account_move_pos_refunded_invoice_ids(env):
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO refunded_invoices (refund_account_move, original_account_move)
        SELECT am.id as refund_account_move, am2.id as original_account_move
        FROM account_move am
        JOIN pos_order pos ON pos.account_move = am.id
        JOIN pos_order_line pol ON pol.order_id = pos.id
        JOIN pos_order_line pol2 ON pol.refunded_orderline_id = pol2.id
        JOIN pos_order pos2 ON pol2.order_id = pos2.id
        JOIN account_move am2 ON pos2.account_move = am2.id
        GROUP BY am.id, am2.id""",
    )


def fill_pos_order_shipping_date(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE pos_order pos
        SET shipping_date = date_order
        WHERE to_ship
        """,
    )


def product_template_convert_pos_categ_id_m2o_to_m2m(env):
    openupgrade.m2o_to_x2m(
        env.cr,
        env["product.template"],
        "product_template",
        "pos_categ_ids",
        "pos_categ_id",
    )


@openupgrade.migrate()
def migrate(env, version):
    fill_account_move_pos_refunded_invoice_ids(env)
    fill_pos_order_shipping_date(env)
    product_template_convert_pos_categ_id_m2o_to_m2m(env)
    openupgrade.load_data(env, "point_of_sale", "17.0.1.0.1/noupdate_changes.xml")
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "point_of_sale.rule_pos_account_move_line",
            "point_of_sale.rule_pos_account_move",
        ],
    )
