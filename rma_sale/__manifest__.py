# Copyright 2020 Tecnativa - Ernesto Tejeda
# Copyright 2022-2023 Tecnativa - Víctor Martínez
# Copyright 2021-2023 Tecnativa - David Vidal
# Copyright 2021-2023 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Return Merchandise Authorization Management - Link with Sales",
    "summary": "Sale Order - Return Merchandise Authorization (RMA)",
    "version": "16.0.1.0.0",
    "development_status": "Production/Stable",
    "category": "RMA",
    "website": "https://github.com/OCA/rma",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["ernestotejeda"],
    "license": "AGPL-3",
    "depends": ["rma", "sale_stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/account_move_views.xml",
        "views/report_rma.xml",
        "views/rma_views.xml",
        "views/sale_views.xml",
        "views/sale_portal_template.xml",
        "views/res_config_settings_views.xml",
        "wizard/sale_order_rma_wizard_views.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "/rma_sale/static/src/js/rma_portal_form.js",
            "/rma_sale/static/src/scss/rma_sale.scss",
        ],
        "web.assets_tests": [
            "/rma_sale/static/src/tests/*.js",
        ],
    },
}
