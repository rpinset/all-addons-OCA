# Copyright 2025 Teacnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)


def post_init_hook(env):
    stages = env["crm.stage"].search([("team_id", "!=", False)])
    for stage in stages:
        stage.write({"team_ids": [(6, 0, stage.team_id.ids)]})
