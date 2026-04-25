# Copyright 2025 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def _assign_journal_xmlids(env):
    """
    Starting in Odoo 17, Odoo expects journals to get external id
    like account.1_sale for sale journal on company 1
    We therefore assign xmlids to existing journals so that they will not be recreated
    """
    for company in env["res.company"].search([("chart_template", "!=", False)]):
        template_data = env["account.chart.template"]._get_chart_template_data(
            company.chart_template
        )
        existing_journals = (
            env["account.journal"]
            .with_context(active_test=False)
            .search(env["account.journal"]._check_company_domain(company), order="id")
        )
        for xmlid, journal_data in list(
            template_data.get("account.journal", {}).items()
        ):
            if not env.ref(xmlid, raise_if_not_found=False) and "type" in journal_data:
                journal = existing_journals.filtered(
                    lambda j: j.type == journal_data["type"]  # noqa: B023
                )[:1]
                if journal:
                    existing_journals -= journal
                    env["ir.model.data"]._update_xmlids(
                        [
                            {
                                "xml_id": f"account.{company.id}_{xmlid}",
                                "record": journal,
                                "noupdate": True,
                            }
                        ]
                    )


@openupgrade.migrate()
def migrate(env, version):
    _assign_journal_xmlids(env)
