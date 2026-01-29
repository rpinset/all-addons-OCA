# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "RMA Sale Delivery",
    "version": "18.0.1.0.0",
    "category": "RMA",
    "website": "https://github.com/OCA/rma",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": ["rma_sale", "rma_delivery"],
    "data": [
        "wizard/sale_order_rma_wizard_views.xml",
    ],
    "maintainers": ["victoralmau"],
}
