# Copyright 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def update_bank_journals(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        ajo = env["account.journal"]
        journals = ajo.search([("type", "=", "bank")])
        sdd_00 = env.ref("l10n_it_sdd_cbi.cbi_sdd_italy_00_01_00")
        if sdd_00:
            journals.write({"inbound_payment_method_ids": [(4, sdd_00.id)]})
        sdd_01 = env.ref("l10n_it_sdd_cbi.cbi_sdd_italy_00_01_01")
        if sdd_01:
            journals.write({"inbound_payment_method_ids": [(4, sdd_01.id)]})
    return
