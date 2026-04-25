# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def _ir_act_server_update_name_if_base_automation(env):
    langs = env["res.lang"].search([]).mapped("code")

    act_servers = (
        env["ir.actions.server"]
        .with_context(active_test=False)
        .search([("base_automation_id", "!=", False)])
    )
    if act_servers:
        for lang in langs:
            act_servers.with_context(lang=lang)._compute_name()


@openupgrade.migrate()
def migrate(env, version):
    _ir_act_server_update_name_if_base_automation(env)
