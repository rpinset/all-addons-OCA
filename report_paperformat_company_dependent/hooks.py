# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    companies = env["res.company"].search([])
    reports = env["ir.actions.report"].with_context(active_test=False).search([])
    for report in reports:
        default_value = report.paperformat_id
        if not default_value:
            continue
        for company in companies:
            report.with_company(company).paperformat_id = default_value
