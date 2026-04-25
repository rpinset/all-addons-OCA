# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreement Helpdesk Mgmt Fieldservice",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/agreement",
    "depends": [
        # oca/agreement
        "agreement_helpdesk_mgmt",
        # oca/helpdesk
        "helpdesk_mgmt_fieldservice",
        # oca/field-service
        "fieldservice_agreement",
    ],
    "auto_install": True,
}
