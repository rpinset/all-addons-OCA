# Copyright 2025 Moduon Team S.L. <info@moduon.team>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openupgradelib import openupgrade


def migrate(cr, version):
    """Rename Product Packaging Quantity Done columns."""
    if openupgrade.column_exists(cr, "stock_move", "product_packaging_qty_done"):
        openupgrade.rename_columns(
            cr,
            {
                "stock_move": [
                    ("product_packaging_qty_done", "product_packaging_quantity"),
                ],
            },
        )
    if openupgrade.column_exists(cr, "stock_move_line", "product_packaging_qty_done"):
        openupgrade.rename_columns(
            cr,
            {
                "stock_move_line": [
                    ("product_packaging_qty_done", "product_packaging_quantity"),
                ],
            },
        )
