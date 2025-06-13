# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Estratti conto cliente con ricevute bancarie",
    "version": "14.0.1.1.0",
    "author": "PyTech, Odoo Community Association (OCA)",
    "category": "Localization/Italy",
    "summary": "Visualizzare le RiBa negli estratti conto cliente.",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_ricevute_bancarie",
        "partner_statement",
    ],
    "data": [
        "reports/outstanding_statement.xml",
        "wizards/outstanding_statement_views.xml",
    ],
}
