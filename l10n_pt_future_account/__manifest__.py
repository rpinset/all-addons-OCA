# Copyright 2025 Open Source Integrators
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'Portugal - Future Accounting Features',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Future accounting features for Portugal',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-portugal',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'l10n_pt',
    ],
    'data': [
        'views/report_invoice.xml',
    ],
    'installable': True,
}
