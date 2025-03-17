#  Copyright 2025 Sergio Zanchetta
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_move_line aml
        SET
            is_stamp_line = True
        FROM account_move am
        WHERE
            aml.move_id = am.id AND
            am.tax_stamp = True AND
            aml.invoice_id is NULL AND
            aml.display_type is NULL;
    """,
    )
