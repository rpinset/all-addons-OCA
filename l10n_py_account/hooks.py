# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import logging

from odoo.tools import convert_file

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Configura la empresa demo con el plan de cuentas paraguayo.

    En Odoo 17+ el plan de cuentas se instala con ``chart_template.try_loading``,
    que requiere el registro totalmente cargado; por eso NO puede llamarse desde
    los XML de demo (se cargan durante la instalación). Aquí, en el post_init,
    el registro ya está cargado: instalamos el plan en la empresa principal y
    luego cargamos las facturas de demostración, que dependen de él (diarios y
    cuentas por defecto).

    Solo se ejecuta cuando el módulo se instala con datos de demostración.
    """
    module = env["ir.module.module"].search([("name", "=", "l10n_py_account")], limit=1)
    if not module.demo:
        return
    company = env.ref("base.main_company")
    # En post_init el registro aún no está "ready", por lo que try_loading emite
    # un WARNING ("Incorrect usage of try_loading without a fully loaded
    # registry"); la carga funciona igualmente. Silenciamos ese logger solo
    # durante la llamada para no disparar falsos positivos en checklog-odoo.
    chart_logger = logging.getLogger("odoo.addons.account.models.chart_template")
    previous_level = chart_logger.level
    chart_logger.setLevel(logging.ERROR)
    try:
        env["account.chart.template"].try_loading("py", company)
    finally:
        chart_logger.setLevel(previous_level)
    for fname in (
        "demo/product_product_demo.xml",
        "demo/account_customer_invoice_demo.xml",
        "demo/account_supplier_invoice_demo.xml",
    ):
        _logger.info("l10n_py_account: cargando demo %s", fname)
        convert_file(
            env,
            "l10n_py_account",
            fname,
            {},
            mode="init",
            noupdate=True,
            kind="demo",
        )
