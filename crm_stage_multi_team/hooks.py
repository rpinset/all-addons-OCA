# Copyright 2025 Teacnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    stages = env["crm.stage"].search([("team_id", "!=", False)])
    for stage in stages:
        stage.write({"team_ids": [(6, 0, stage.team_id.ids)]})
