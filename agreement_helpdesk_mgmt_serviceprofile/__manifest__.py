# Copyright 2020 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreement Helpdesk Mgmt ",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Open Source Integrators,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/agreement",
    "depends": [
        "agreement_helpdesk_mgmt",
        "agreement_serviceprofile",
    ],
    "data": [
        "views/helpdesk_ticket.xml",
    ],
    "auto_install": True,
    "maintainers": ["bodedra"],
}
