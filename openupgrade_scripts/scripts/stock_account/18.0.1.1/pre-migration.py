# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def delete_property_xmlids(env):
    # avoid conflict in in _create_default_stock_accounts_properties
    # they changed records from ir.property to ir.default
    for field in [
        "property_stock_account_output_categ_id",
        "property_stock_account_input_categ_id",
    ]:
        imd = env["ir.model.data"].search(
            [("module", "=", "stock_account"), ("name", "=", field)]
        )
        if imd:
            imd.unlink()


@openupgrade.migrate()
def migrate(env, version):
    delete_property_xmlids(env)
