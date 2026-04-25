# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def _normalize_start_end_dates(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE mrp_production
        SET date_start = COALESCE(date_planned_start, create_date)
        WHERE date_start IS NULL
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE mrp_production
        SET date_finished = date_planned_finished
        WHERE date_finished IS NULL
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE mrp_workorder
        SET date_start = date_planned_start
        WHERE date_start IS NULL AND date_planned_start IS NOT NULL
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE mrp_workorder
        SET date_finished = date_planned_finished
        WHERE date_finished IS NULL
        """,
    )


def _prefill_mrp_workorder_barcode(env):
    openupgrade.logged_query(env.cr, "ALTER TABLE mrp_workorder ADD barcode VARCHAR")
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE mrp_workorder mw
        SET barcode = mp.name || mw.id::varchar
        FROM mrp_production mp
        WHERE mp.id = mw.production_id
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    _normalize_start_end_dates(env)
    _prefill_mrp_workorder_barcode(env)
