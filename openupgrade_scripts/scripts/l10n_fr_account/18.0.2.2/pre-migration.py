# Copyright 2025 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

model_renames = [
    ("account.fr.fec", "l10n_fr.fec.export.wizard"),
]

table_renames = [
    ("account_fr_fec", "l10n_fr_fec_export_wizard"),
]


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.table_exists(env.cr, "account_fr_fec"):
        openupgrade.rename_models(env.cr, model_renames)
        openupgrade.rename_tables(env.cr, table_renames)
        openupgrade.delete_records_safely_by_xml_id(
            env, ["l10n_fr_fec.account_fr_fec_rule"]
        )
