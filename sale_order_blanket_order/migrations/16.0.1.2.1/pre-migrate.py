from odoo.tools import sql


def migrate(cr, version):
    # blanket_strict_packaging is added in both sale_order and sale_order_line to
    # avoid computing the field for all records at module install
    if not sql.column_exists(cr, "sale_order", "blanket_strict_packaging"):
        cr.execute("ALTER TABLE sale_order ADD COLUMN blanket_strict_packaging BOOLEAN")

    if not sql.column_exists(cr, "sale_order_line", "blanket_strict_packaging"):
        cr.execute(
            "ALTER TABLE sale_order_line ADD COLUMN blanket_strict_packaging BOOLEAN"
        )
