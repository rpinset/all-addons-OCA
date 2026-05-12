# Copyright 2026 Therp BV (https://therp.nl)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    sct_method = env.ref("account_banking_sepa_credit_transfer.sepa_credit_transfer")
    sct_method.write(
        {
            "pain_version": "pain.001.001.09",
            "warn_not_sepa": True,
        }
    )
