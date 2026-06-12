# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "EDI Notification",
    "summary": """Define notification activities on exchange records.""",
    "version": "19.0.1.0.0",
    "development_status": "Alpha",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/edi-framework",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "depends": ["edi_core_oca"],
    "data": [
        "data/mail_activity_type.xml",
        "data/edi_configuration.xml",
        "views/edi_exchange_type.xml",
    ],
    "installable": True,
}
