# Copyright 2022 ACSONE SA/NV
# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not openupgrade.table_exists(env.cr, "product_packaging_type"):
        return
    # Former version of the module is present
    openupgrade.rename_models(
        env.cr, [("product.packaging.type", "product.packaging.level")]
    )
    openupgrade.rename_tables(
        env.cr, [("product_packaging_type", "product_packaging_level")]
    )
    fields = [
        (
            "product.packaging",
            "product_packaging",
            "packaging_type_id",
            "packaging_level_id",
        )
    ]
    openupgrade.rename_fields(env, fields, no_deep=True)
    openupgrade.rename_xmlids(
        env.cr,
        [
            (
                "product_packaging_level.product_packaging_type_default",
                "product_packaging_level.product_packaging_level_default",
            )
        ],
    )
