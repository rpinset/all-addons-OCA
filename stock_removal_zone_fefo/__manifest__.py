# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Removal Zone-Level FEFO",
    "summary": "Removal strategy expiring goods first, then goods that entered"
    " a storage zone first",
    "version": "18.0.1.0.0",
    "author": "Camptocamp, BCIM, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/stock-logistics-reservation",
    "category": "Stock Management",
    "depends": ["stock_removal_zone_fifo", "product_expiry"],
    "data": ["data/stock_removal_data.xml"],
    "auto_install": True,
    "installable": True,
    "development_status": "Beta",
    "license": "AGPL-3",
    "maintainers": ["jbaudoux"],
}
