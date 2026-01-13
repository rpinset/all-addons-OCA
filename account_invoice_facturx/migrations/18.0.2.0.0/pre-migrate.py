# Copyright 2026 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # this inherited view has been removed with 2.0.0
    # without this script other unrelated modules may
    # break when updating the settings view
    openupgrade.delete_records_safely_by_xml_id(
        env,
        ["account_invoice_facturx.view_account_config_settings"],
        delete_childs=True,
    )
