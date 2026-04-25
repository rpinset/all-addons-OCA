# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Helpdesk Ticket Equipment Warranty",
    "summary": "Helpdesk Ticket Equipment Warranty",
    "version": "18.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/helpdesk",
    "license": "AGPL-3",
    "category": "HelpDesk Service",
    "depends": [
        "helpdesk_mgmt_fieldservice_equipment",
        # oca/field-service
        "fieldservice_equipment_warranty",
    ],
    "data": [
        "views/helpdesk_ticket.xml",
    ],
}
