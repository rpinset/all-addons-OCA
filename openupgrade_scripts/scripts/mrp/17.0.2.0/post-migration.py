# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def _transfer_delays_from_product_to_bom(env):
    """As the product template is required in BoMs, a simple cross-link update is
    enough.
    """
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE mrp_bom mb
        SET days_to_prepare_mo = pt.days_to_prepare_mo
        FROM product_template pt
        WHERE pt.id = mb.product_tmpl_id
            AND pt.days_to_prepare_mo <> 0
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE mrp_bom mb
        SET produce_delay = pt.produce_delay
        FROM product_template pt
        WHERE pt.id = mb.product_tmpl_id
            AND pt.produce_delay <> 0
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    _transfer_delays_from_product_to_bom(env)
