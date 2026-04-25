# Copyright (C) 2024 APSL-Nagarro Antoni Marroig
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not openupgrade.table_exists(env.cr, "repair_type"):
        return
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE stock_picking_type
        ADD COLUMN old_repair_type_id_legacy INTEGER;
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        SELECT rt.destination_location_add_part_id,
            rt.destination_location_remove_part_id,
            rt.name,
            rt.source_location_add_part_id,
            rt.source_location_remove_part_id,
            sl.company_id,
            rt.id
        FROM repair_type rt
        LEFT JOIN stock_location sl ON sl.id = rt.source_location_add_part_id
        ORDER BY rt.create_date;
        """,
    )
    for (
        destination_location_add_part_id,
        destination_location_remove_part_id,
        rt_name,
        source_location_add_part_id,
        source_location_remove_part_id,
        company_id,
        rt_id,
    ) in env.cr.fetchall():
        pt = env["stock.picking.type"].create(
            {
                "name": rt_name,
                "code": "repair_operation",
                "sequence_code": rt_name[:2].upper() + str(rt_id),
                "default_location_dest_id": destination_location_add_part_id,
                "default_remove_location_dest_id": destination_location_remove_part_id,
                "default_add_location_src_id": source_location_add_part_id,
                "default_remove_location_src_id": source_location_remove_part_id,
                "company_id": company_id,
            }
        )
        openupgrade.logged_query(
            env.cr,
            """
                UPDATE stock_picking_type spt
                SET old_repair_type_id_legacy = %s
                WHERE id = %s;
            """,
            (rt_id, pt.id),
        )

    openupgrade.logged_query(
        env.cr,
        """
            UPDATE repair_order ro
            SET picking_type_id = spt.id
            FROM stock_picking_type spt
            WHERE ro.repair_type_id = spt.old_repair_type_id_legacy;
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE repair_order
        DROP COLUMN repair_type_id;
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        DROP TABLE repair_type;
        """,
    )
