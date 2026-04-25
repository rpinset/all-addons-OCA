# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "website_forum", "17.0.1.2/noupdate_changes.xml")
    openupgrade.set_xml_ids_noupdate_value(
        env, "website_forum", ["action_open_forum", "forum_post_view_kanban"], True
    )
