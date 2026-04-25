# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

RENAMED_XMLIDS = [
    (
        "spreadsheet_dashboard_event_sale.spreadsheet_dashboard_group_marketing",
        "spreadsheet_dashboard.spreadsheet_dashboard_group_marketing",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, RENAMED_XMLIDS)
