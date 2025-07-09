# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Ricevute bancarie - Asincrono",
    "version": "14.0.1.1.0",
    "author": "PyTech, Odoo Community Association (OCA)",
    "category": "Localization/Italy",
    "summary": "Pagare righe RiBa in modo asincrono.",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_ricevute_bancarie",
        "queue_job",
    ],
    "data": [
        "wizards/wizard_riba_multiple_payment_views.xml",
    ],
}
