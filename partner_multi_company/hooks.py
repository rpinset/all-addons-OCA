from odoo import SUPERUSER_ID, api

from odoo.addons.base_multi_company import hooks


def post_init_hook(cr, registry):
    """Keep multi-company behavior for partners."""
    hooks.fill_company_ids(cr, "res.partner")
    fix_user_partner_companies(cr)


def fix_user_partner_companies(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for user in env["res.users"].search([]):
        user_company_ids = set(user.company_ids.ids)
        partner_company_ids = set(user.partner_id.company_ids.ids)
        if not user_company_ids.issubset(partner_company_ids) and partner_company_ids:
            missing_company_ids = list(user_company_ids - partner_company_ids)
            user.partner_id.write(
                {"company_ids": [(4, company_id) for company_id in missing_company_ids]}
            )
