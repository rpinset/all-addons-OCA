# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

{
    "name": "ITA - Ritenute d'acconto - MIS Builder",
    "version": "14.0.1.0.0",
    "category": "Account",
    "author": "PyTech SRL, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_withholding_tax",
        "mis_builder",
    ],
    "data": [
        "views/account_move_line_view.xml",
    ],
    "pre_init_hook": "pre_init_hook",
}
