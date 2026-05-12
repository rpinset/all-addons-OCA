# Copyright 2016-2020 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2026 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import SUPERUSER_ID, api


def update_bank_journals(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    sct = env.ref("account_banking_sepa_credit_transfer.sepa_credit_transfer")
    journals = env["account.journal"].search([("type", "=", "bank")])
    for journal in journals:
        if sct not in journal.outbound_payment_method_line_ids.payment_method_id:
            journal.write(
                {
                    "outbound_payment_method_line_ids": [
                        (0, 0, {"payment_method_id": sct.id})
                    ]
                }
            )
    return
