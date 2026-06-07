# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def pre_absorb_old_module(env):
    if openupgrade.is_module_installed(env.cr, "l10n_it_vat_statement_communication"):
        openupgrade.update_module_names(
            env.cr,
            [
                (
                    "l10n_it_vat_statement_communication",
                    "l10n_it_vat_settlement_communication",
                ),
            ],
            merge_modules=True,
        )


def post_absorb_old_module(env):
    """Migrate v16 ``vsc_exclude_operation`` to the v18 split fields.

    In v16 (l10n_it_vat_statement_communication) there was a single
    ``vsc_exclude_operation`` Boolean on account.tax.  In v18 it has
    been replaced by two separate fields:
    ``vsc_exclude_active_operation`` and ``vsc_exclude_passive_operation``.

    This hook copies the old value into both new columns so that taxes
    excluded in v16 remain excluded in v18.
    """
    if openupgrade.column_exists(env.cr, "account_tax", "vsc_exclude_operation"):
        env.cr.execute(
            """
            UPDATE account_tax
            SET vsc_exclude_active_operation = vsc_exclude_operation,
                vsc_exclude_passive_operation = vsc_exclude_operation
            WHERE vsc_exclude_operation = True
            """
        )
