# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Invoicing Date From Picking",
    "summary": "Applies the wizard date to invoices generated from pickings",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "category": "Accounting & Finance",
    "website": "https://github.com/OCA/account-invoicing",
    "author": "Sygel, Odoo Community Association (OCA)",
    "depends": [
        "sale_invoicing_date_selection",
        "sale_order_invoicing_picking_filter",
    ],
    "installable": True,
}
