# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    l10n_be_xmlids = [
        "tax_group_tva_0",
        "tax_group_tva_12",
        "tax_group_tva_21",
        "tax_group_tva_6",
    ]
    openupgrade.delete_records_safely_by_xml_id(
        env, [f"l10n_be.{x}" for x in l10n_be_xmlids]
    )
