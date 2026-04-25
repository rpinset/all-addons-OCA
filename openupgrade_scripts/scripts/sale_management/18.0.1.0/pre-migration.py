# Copyright 2025 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def _fill_sale_order_template_sequence(env):
    openupgrade.logged_query(
        env.cr,
        """
         ALTER TABLE sale_order_template ADD COLUMN IF NOT EXISTS sequence INTEGER
         """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE sale_order_template
        SET sequence = id
        WHERE sequence IS NULL
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    _fill_sale_order_template_sequence(env)
