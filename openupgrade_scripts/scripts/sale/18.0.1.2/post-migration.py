# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "sale", "18.0.1.2/noupdate_changes.xml")
    openupgrade.delete_record_translations(
        env.cr, "sale", ["email_template_edi_sale", "mail_template_sale_confirmation"]
    )
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "sale.account_invoice_send_rule_see_all",
            "sale.account_invoice_send_rule_see_personal",
            "sale.onboarding_onboarding_step_sale_order_confirmation",
            "sale.onboarding_onboarding_step_sample_quotation",
            "sale.onboarding_onboarding_sale_quotation",
        ],
    )
