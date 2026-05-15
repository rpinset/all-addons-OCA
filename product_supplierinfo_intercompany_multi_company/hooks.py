import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.base_multi_company import hooks
except ImportError:
    _logger.info("Cannot find `base_multi_company` module in addons path.")


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    hooks.set_security_rule(env, "product.product_supplierinfo_comp_rule")


def uninstall_hook(cr, registry):
    hooks.uninstall_hook(
        cr,
        "product.product_supplierinfo_comp_rule",
    )
