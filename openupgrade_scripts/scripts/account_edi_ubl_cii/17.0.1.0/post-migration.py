# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    xmlids = [
        "edi_efff_1",
        "edi_facturx_1_0_05",
        "edi_nlcius_1",
        "edi_ubl_2_1",
        "ubl_a_nz",
        "ubl_bis3",
        "ubl_de",
        "ubl_sg",
    ]
    openupgrade.delete_records_safely_by_xml_id(
        env, [f"account_edi_ubl_cii.{x}" for x in xmlids]
    )
