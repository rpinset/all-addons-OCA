from openupgradelib import openupgrade

# pylint: disable=odoo-addons-relative-import
from odoo.addons.product_supplierinfo_intercompany_multi_company.hooks import (
    post_init_hook,
)


@openupgrade.migrate()
def migrate(env, version):
    post_init_hook(env.cr, env.registry)
