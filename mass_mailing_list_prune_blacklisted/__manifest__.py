# Copyright 2026 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Remove blacklisted emails from Mass Mailing Lists",
    "summary": "Allow to remove blacklisted emails from mailing lists.",
    "version": "16.0.1.0.0",
    "category": "Marketing",
    "website": "https://github.com/OCA/social",
    "author": "PyTech, Odoo Community Association (OCA)",
    "maintainers": [
        "SirPyTech",
    ],
    "license": "AGPL-3",
    "depends": [
        "mass_mailing",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/mailing_mailing_views.xml",
        "wizards/prune_mailing_list_views.xml",
    ],
}
