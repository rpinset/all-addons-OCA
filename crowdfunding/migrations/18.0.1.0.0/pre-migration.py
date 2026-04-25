from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version=None):
    openupgrade.rename_xmlids(
        env.cr,
        [
            ("crowdfunding.transaction_form", "crowdfunding.payment_transaction_form"),
        ],
    )
