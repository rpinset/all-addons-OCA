# Copyright 2024,2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

_field_renames = [
    ("crm.lead", "crm_lead", "date_action_last", "date_automation_last"),
]


def _fill_crm_lead_recurring_revenue_prorated(env):
    openupgrade.logged_query(
        env.cr, "ALTER TABLE crm_lead ADD recurring_revenue_prorated NUMERIC"
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE crm_lead
        SET recurring_revenue_prorated = (
            COALESCE(recurring_revenue, 0) * COALESCE(probability, 0)
        ) / 100
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    _fill_crm_lead_recurring_revenue_prorated(env)
    openupgrade.rename_fields(env, _field_renames)
