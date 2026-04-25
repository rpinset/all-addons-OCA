# Copyright 2025 Open Source Integrators
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Portugal - Payment Methods",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations/Payment Methods",
    "summary": "Portugal-specific payment methods: Multibanco and MB WAY",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-portugal",
    "license": "LGPL-3",
    "depends": ["payment", "l10n_pt"],
    "data": [
        "data/payment_method_data.xml",
    ],
    "installable": True,
    "auto_install": True,
}
