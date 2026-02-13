# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class ContractManuallyCreateInvoice(models.TransientModel):
    _inherit = "contract.manually.create.invoice"

    filter_domain = fields.Char(
        string="Domain",
        compute="_compute_filter_domain",
        store=True,
        readonly=False,
        help="Filter/Domain to apply on contracts to invoice",
    )

    @api.depends("invoice_date", "contract_type")
    def _compute_filter_domain(self):
        for wizard in self:
            domain = [
                (
                    "recurring_next_date",
                    "<=",
                    fields.Datetime.to_string(wizard.invoice_date),
                ),
                ("contract_type", "=", wizard.contract_type),
            ]
            if self.env.company.enable_contract_invoice_manually:
                domain = expression.AND([domain, [("is_manually_invoiced", "=", True)]])
            wizard.filter_domain = str(domain)

    @api.depends("invoice_date", "filter_domain")
    def _compute_contract_to_invoice_ids(self):
        """
        Overwrite domain
        """
        super()._compute_contract_to_invoice_ids()
        Contract = self.env["contract.contract"]
        for wizard in self:
            contracts = Contract.search(safe_eval(wizard.filter_domain))
            wizard.contract_to_invoice_ids = contracts
            wizard.contract_to_invoice_count = len(contracts)
        return
