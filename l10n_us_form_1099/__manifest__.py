# Copyright (C) 2017-2024 Open Source Integrators
# Copyright (C) 2019-2024 Brian McMaster
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "US Form 1099",
    "version": "17.0.1.0.0",
    "author": "Open Source Integrators, "
    "Brian McMaster, "
    "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "summary": "Manage 1099 Types and Suppliers",
    "category": "Customers",
    "maintainer": "Open Source Integrators",
    "website": "https://github.com/OCA/l10n-usa",
    "depends": ["contacts", "account"],
    "data": [
        "data/type_1099_data.xml",
        "data/box_1099_misc_data.xml",
        "security/ir.model.access.csv",
        "views/type_1099_views.xml",
        "views/box_1099_misc_views.xml",
        "views/res_partner_views.xml",
        "reports/account_payment_1099_report_views.xml",
    ],
    "installable": True,
    "development_status": "Production/Stable",
    "maintainers": ["max3903"],
}
