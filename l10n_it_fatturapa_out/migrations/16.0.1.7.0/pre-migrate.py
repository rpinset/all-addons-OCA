# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def precompute_new_computed_fields(env):
    openupgrade.add_fields(
        env,
        [
            (
                "fatturapa_payment_method_id",
                "account.move",
                False,  # Model already loaded
                "many2one",  # Odoo field type
                False,  # SQL type retrieved from Odoo field type
                "l10n_it_fatturapa_out",
            ),
            (
                "fatturapa_payment_term_id",
                "account.move",
                False,  # Model already loaded
                "many2one",  # Odoo field type
                False,  # SQL type retrieved from Odoo field type
                "l10n_it_fatturapa_out",
            ),
        ],
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE
            account_move am
        SET
            fatturapa_payment_method_id = apt.fatturapa_pm_id,
            fatturapa_payment_term_id = apt.fatturapa_pt_id
        FROM
            account_payment_term apt
        WHERE
            apt.id = am.invoice_payment_term_id
            AND am.fatturapa_attachment_out_id is not NULL
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    precompute_new_computed_fields(env)
