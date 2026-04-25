# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def _remove_xml_id_account_fiscal_position(env):
    """In 17.0 account.fiscal.position.tax and account.fiscal.position.account don't
    have XML-IDs. With this method they are removed.
    """
    for company in env["res.company"].search([]):
        openupgrade.logged_query(
            env.cr,
            f"""
            DELETE FROM ir_model_data
            WHERE module='l10n_de'
            AND model IN (
                'account.fiscal.position.tax', 'account.fiscal.position.account'
            ) AND name LIKE '{company.id}_%'
            """,
        )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(
        env.cr,
        [
            ("l10n_de.l10n_de_chart_template", "l10n_de.de_skr03"),
            ("l10n_de.l10n_chart_de_skr04", "l10n_de.de_skr04"),
        ],
    )
    _remove_xml_id_account_fiscal_position(env)
