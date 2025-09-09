#  Copyright 2025 Michele Di Croce - Stesi Consulting
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Clean old transient data
    drop_old_wizard_export_sql = "DELETE FROM wizard_export_fatturapa;"

    openupgrade.logged_query(env.cr, drop_old_wizard_export_sql)
