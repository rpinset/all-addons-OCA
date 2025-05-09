# Copyright 2015-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import SUPERUSER_ID, api

from odoo.addons.base_multi_company import hooks


def post_init_hook(cr, registry):
    api.Environment(cr, SUPERUSER_ID, {})
    hooks.fill_company_ids(cr, "product.template")
