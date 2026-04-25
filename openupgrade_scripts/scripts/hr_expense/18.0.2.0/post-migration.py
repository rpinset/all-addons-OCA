# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "hr_expense", "18.0.2.0/noupdate_changes.xml")
    xml_ids = [
        "hr_expense_template_register",
        "product_product_no_cost",
        "mt_expense_approved",
    ]
    openupgrade.delete_record_translations(env.cr, "hr_expense", xml_ids)
