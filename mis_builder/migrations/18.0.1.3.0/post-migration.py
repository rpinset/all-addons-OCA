# Copyright 2025 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

from odoo.tools.safe_eval import safe_eval


@openupgrade.migrate()
def migrate(cr, version):
    """Update the value of the analytic_domain field."""
    # Workaround to execute the migration script without errors
    # see https://github.com/odoo/odoo/blob/2a839ef1ed09c36f27ce7536ca3052d9f65ceed9/odoo/modules/migration.py#L252-L256
    env = cr
    for record in env["mis.report.instance.period"].search(
        [("analytic_domain", "!=", False)]
    ):
        new_domain = _update_domain(record)
        record.write({"analytic_domain": new_domain})

    for record in env["mis.report.instance"].search([("analytic_domain", "!=", False)]):
        new_domain = _update_domain(record)
        record.write({"analytic_domain": new_domain})


def _update_domain(record):
    # analytic_distribution_search has been removed in v18 and it was set on purpose
    # on mis_builder migration scripts in 16.0.
    domain = safe_eval(record.analytic_domain)
    new_domain = []
    for clause in domain:
        if (
            isinstance(clause, list | tuple)
            and clause[0] == "analytic_distribution_search"
        ):
            operator = clause[1]
            value = clause[2]
            clause = ("distribution_analytic_account_ids", operator, value)
        new_domain.append(clause)
    return new_domain
