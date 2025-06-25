# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    prepayments_type = env.ref(
        "account.data_account_type_prepayments",
        raise_if_not_found=False,
    )
    if prepayments_type and prepayments_type.account_balance_sign == -1:
        prepayments_type.account_balance_sign = 1
