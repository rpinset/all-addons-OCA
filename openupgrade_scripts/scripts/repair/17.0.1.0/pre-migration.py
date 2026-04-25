# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

from odoo.tools import sql


def add_helper_repair_move_rel(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE stock_move
        ADD COLUMN old_repair_line_id integer""",
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE stock_move sm
        SET old_repair_line_id = rl.id
        FROM repair_line rl
        WHERE sm.id = rl.move_id
        """,
    )
    # Create index for these columns, as they are going to be accessed frequently
    index_name = "stock_move_old_repair_line_id_index"
    sql.create_index(env.cr, index_name, "stock_move", ['"old_repair_line_id"'])


def stock_warehouse_create_columns(env):
    """
    Add the repair_type_id column to the stock_warehouse table
    before the default value for the picking_type_id field in repair.order is executed.
    This is necessary because the field is required.
    Even if the field exists, Odoo will execute the default,
    and due to the import order in the repair module,
    the stock.warehouse model has not been processed yet
    and the field does not exist at that point.
    """
    openupgrade.add_columns(
        env, [(False, "repair_type_id", "many2one", None, "stock_warehouse")]
    )


def repair_create_columns(env):
    """Add columns to the repair_order table
    before the default value for the picking_type_id field in repair.order is executed.
    Set a dummy value for the new columns.
    The correct values will be assigned during the post-migration step.
    This is necessary because the fields are required,
    but due to the model loading order,
    the repair_type_id field in the warehouse is still empty.
    """
    openupgrade.add_columns(
        env,
        [
            (False, "picking_type_id", "many2one", None, "repair_order"),
            (False, "location_dest_id", "many2one", None, "repair_order"),
            (False, "parts_location_id", "many2one", None, "repair_order"),
            (False, "recycle_location_id", "many2one", None, "repair_order"),
        ],
    )
    temporal_location = env["stock.location"].create(
        {
            "name": "Temporary Location OpenUpgrade",
            "usage": "transit",
            "company_id": False,
        }
    )
    # Create the picking type
    picking_type = env["stock.picking.type"].create(
        {
            "name": "SPT Repair OpenUpgrade",
            "code": "internal",
            "default_location_src_id": temporal_location.id,
            "default_location_dest_id": temporal_location.id,
            "sequence": 1000,
            "sequence_code": "OU",
        }
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE repair_order
        SET picking_type_id = %(picking_type_id)s,
        location_dest_id = %(location_id)s,
        parts_location_id = %(location_id)s,
        recycle_location_id = %(location_id)s
        """,
        {"picking_type_id": picking_type.id, "location_id": temporal_location.id},
    )


def fill_repair_order_schedule_date(env):
    """
    Set the schedule_date for repair orders where it is currently null.
    The field was not required before, but now it is required,
    to prevent it from defaulting to now(), assign the create_date instead.
    """
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE repair_order
        SET schedule_date = create_date
        WHERE schedule_date IS NULL
        """,
    )


@openupgrade.migrate()
def migrate(env, version=None):
    openupgrade.remove_tables_fks(env.cr, ["repair_line", "repair_fee"])
    openupgrade.copy_columns(env.cr, {"repair_order": [("state", None, None)]})
    add_helper_repair_move_rel(env)
    stock_warehouse_create_columns(env)
    repair_create_columns(env)
    fill_repair_order_schedule_date(env)
