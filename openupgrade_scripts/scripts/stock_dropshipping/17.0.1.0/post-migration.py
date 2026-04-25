# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# Copyright 2025 Tecnativa - Pedro M. Baeza

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Assign the new code to the existing picking types with these characteristics
    env["stock.picking.type"].search(
        [
            ("default_location_src_id.usage", "=", "supplier"),
            ("default_location_dest_id.usage", "=", "customer"),
        ]
    ).code = "dropship"
