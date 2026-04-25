# Copyright 2025 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def _update_pos_payment_method_journal(env):
    """From now on, a journal is required when the transactions aren't splitted. If we
    don't set a journal in these cases, the session closing won't be made properly for
    these methods. Cash payment methos already had a jornal set, but bank ones didn't.
    """
    payment_methods = (
        env["pos.payment.method"]
        .search(
            [
                ("journal_id", "=", False),
                ("split_transactions", "=", False),
            ]
        )
        .filtered_domain([("type", "=", "bank")])
    )
    for i, method in enumerate(payment_methods):
        method.journal_id = env["account.journal"].create(
            {
                "type": "bank",
                "name": f"[openupgrade] Journal for {method.name}",
                "code": "POS%s" % i,
                "company_id": method.company_id.id,
                "sequence": 99,
            }
        )


@openupgrade.migrate()
def migrate(env, version):
    _update_pos_payment_method_journal(env)
