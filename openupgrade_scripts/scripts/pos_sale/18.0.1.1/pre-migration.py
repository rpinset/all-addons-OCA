# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.add_columns(env, [("pos.order.line", "qty_delivered", "float", 0)])
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE pos_order_line pol2
        SET qty_delivered = sub.quantity
        FROM (
            SELECT pol.id, SUM(sm.quantity) as quantity
            FROM pos_order_line pol
            JOIN pos_order po ON pol.order_id = po.id
                AND po.state IN ('paid', 'done', 'invoiced')
            JOIN stock_picking sp ON sp.pos_order_id = po.id
                AND sp.state = 'done'
            JOIN stock_picking_type spt ON sp.picking_type_id = spt.id
                AND spt.code = 'outgoing'
            JOIN stock_move sm ON sm.picking_id = sp.id AND sm.state = 'done'
                AND sm.product_id = pol.product_id
            GROUP BY pol.id
        ) sub
        WHERE sub.id = pol2.id
        """,
    )
