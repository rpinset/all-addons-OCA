# Copyright 2026 Nexusai Solutions (OPC) Private Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Crowdfunding Schedule",
    "summary": "Add start and end datetime scheduling to crowdfunding challenges",
    "version": "18.0.1.0.0",
    "category": "Crowdfunding",
    "author": "OS-SCI, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crowdfunding",
    "license": "AGPL-3",
    "development_status": "Alpha",
    "depends": [
        "crowdfunding",
    ],
    "data": [
        "templates/crowdfunding_schedule.xml",
        "templates/payment.xml",
        "views/crowdfunding_schedule.xml",
    ],
    "demo": ["demo/crowdfunding_challenge.xml"],
    "installable": True,
    "application": False,
}
