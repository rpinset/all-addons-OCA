# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade, openupgrade_180


def convert_company_dependent(env):
    openupgrade_180.convert_company_dependent(
        env, "res.partner", "property_purchase_currency_id"
    )
    openupgrade_180.convert_company_dependent(
        env, "res.partner", "receipt_reminder_email"
    )
    openupgrade_180.convert_company_dependent(
        env, "res.partner", "reminder_date_before_receipt"
    )


@openupgrade.migrate()
def migrate(env, version):
    convert_company_dependent(env)
    openupgrade.load_data(env, "purchase", "18.0.1.2/noupdate_changes.xml")
    openupgrade.delete_record_translations(
        env.cr, "purchase", ["email_template_edi_purchase", "track_po_line_template"]
    )
    openupgrade.delete_records_safely_by_xml_id(
        env,
        ["purchase.receipt_reminder_email", "purchase.reminder_date_before_receipt"],
    )
