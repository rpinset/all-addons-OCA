# Copyright 2025 Therp BV (https://www.therp.nl).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def migrate_partner_coc(env):
    """Migrate the id number of the now non-existent module partner_coc."""
    openupgrade.logged_query(
        env.cr,
        """
        WITH xmlid AS (
            SELECT res_id AS id FROM ir_model_data
            WHERE module = 'partner_coc' AND name = 'id_category_coc'
            LIMIT 1
        )
        UPDATE res_partner rp SET company_registry = r.name
        FROM (
            SELECT partner_id, name FROM res_partner_id_number
            WHERE category_id = (SELECT id FROM xmlid)
        ) AS r
        WHERE rp.id = r.partner_id;
        """,
    )


@openupgrade.migrate()
def migrate(env, _):
    migrate_partner_coc(env)
