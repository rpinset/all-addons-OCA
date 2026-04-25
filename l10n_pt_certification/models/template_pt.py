# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @template('pt', 'account.journal')
    def _get_pt_account_account_journal(self):
        """
        Different AT Series are needed for invoices and refunds. For consistency, have a dedicated sequence
        for refunds by default.
        """
        return {
            'sale': {
                'refund_sequence': True,
            },
        }

    @template('pt', 'account.tax')
    def _get_pt_certification_account_tax(self):
        return self._parse_csv('pt', 'account.tax', module='l10n_pt_certification')

    @template('pt', 'account.tax.group')
    def _get_pt_certification_account_tax_group(self):
        return self._parse_csv('pt', 'account.tax.group', module='l10n_pt_certification')
