# Copyright 2025 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website Sale Stock Order Cancel",
    "version": "15.0.1.0.0",
    "summary": "Enhances website sale order cancellation by "
    "blocking it when related stock pickings are done.",
    "category": "Website",
    "website": "https://github.com/OCA/e-commerce",
    "author": "APSL-Nagarro, Odoo Community Association (OCA)",
    "maintainers": ["ppyczko"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website_sale_order_cancel", "website_sale_stock"],
}
