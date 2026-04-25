# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade, openupgrade_180


def convert_company_dependent(env):
    openupgrade_180.convert_company_dependent(env, "res.users", "property_warehouse_id")


@openupgrade.migrate()
def migrate(env, version):
    convert_company_dependent(env)
