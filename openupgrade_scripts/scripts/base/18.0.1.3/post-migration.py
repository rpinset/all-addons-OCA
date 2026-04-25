# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade, openupgrade_180


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "base", "18.0.1.3/noupdate_changes.xml")
    openupgrade_180.convert_company_dependent(env, "res.partner", "barcode")
    openupgrade.delete_records_safely_by_xml_id(
        env, ["base.module_sale_ebay", "base.module_website_twitter_wall"]
    )
    enterprise_old = env.ref("base.module_account_accountant", raise_if_not_found=False)
    env["ir.model.data"].search(
        [("module", "=", "base"), ("name", "=", "module_account_accountant")]
    ).unlink()
    enterprise_new = env.ref("base.module_accountant", raise_if_not_found=False)
    if (
        enterprise_old
        and enterprise_new
        and enterprise_old.state in ("to install", "to upgrade")
    ):
        enterprise_new.state = "to install"
