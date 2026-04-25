# Copyright (C) 2025 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from openupgradelib import openupgrade  # pylint: disable=W7936

_field_renames = [
    ("stock.warehouse", "stock_warehouse", "remove_c_type_id", "recycle_c_type_id"),
]


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    # Rename operation types
    for wh in env["stock.warehouse"].search([]):
        if hasattr(wh, "remove_c_type_id") and wh.remove_c_type_id:
            wh.recycle_c_type_id.name = wh.recycle_c_type_id.name.replace(
                "Remove", "Recycle"
            )
    # Rename fields
    for field in _field_renames:
        if openupgrade.table_exists(cr, field[1]) and openupgrade.column_exists(
            cr, field[1], field[2]
        ):
            openupgrade.rename_fields(env, _field_renames)
