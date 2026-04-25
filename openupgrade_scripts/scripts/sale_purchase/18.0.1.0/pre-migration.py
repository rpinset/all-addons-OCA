# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(env.cr, "product_template", "service_to_purchase"):
        # in v15, the field was not company_dependent
        openupgrade.rename_columns(
            env.cr,
            {"product_template": [("service_to_purchase", None)]},
        )
