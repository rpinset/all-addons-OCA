# Copyright 2024 Viindoo Technology Joint Stock Company (Viindoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def _company_update_company_expense_allowed_payment_method_line(env):
    env.cr.execute(
        """
        SELECT id, company_expense_journal_id FROM res_company company
        """
    )
    for company_id, company_expense_journal_id in env.cr.fetchall():
        company = env["res.company"].browse(company_id)
        if company_expense_journal_id:
            journal = env["account.journal"].browse(company_expense_journal_id)
            company.company_expense_allowed_payment_method_line_ids = (
                journal.outbound_payment_method_line_ids
            )


@openupgrade.migrate()
def migrate(env, version):
    _company_update_company_expense_allowed_payment_method_line(env)
    openupgrade.load_data(env, "hr_expense", "17.0.2.0/noupdate_changes.xml")
    openupgrade.delete_record_translations(
        env.cr,
        "hr_expense",
        (
            "hr_expense_template_refuse_reason",
            "hr_expense_template_register",
            "hr_expense_template_register_no_user",
        ),
    )
