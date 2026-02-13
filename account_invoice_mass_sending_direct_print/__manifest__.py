# Copyright 2025 CamptoCamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Mass Sending Direct Print",
    "summary": """
        This addon adds a mass sending direct print feature on invoices.""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "CamptoCamp, Odoo Community Association (OCA), Open Net Sàrl",
    "website": "https://github.com/OCA/account-invoicing",
    "depends": [
        "base_report_to_printer",
        "account_invoice_mass_sending",
    ],
    "data": [
        "views/res_config_settings_views.xml",
        "wizards/account_invoice_send.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
