# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tools.sql import column_exists


def migrate(cr, version):
    """Name Search became the Documents filter. Carry each search over as a
    filter on the display name, which is what the name search matched."""
    if not column_exists(cr, "tier_correction", "search_name"):
        return
    cr.execute(
        "SELECT id, search_name FROM tier_correction "
        "WHERE search_name IS NOT NULL AND search_name != ''"
    )
    for correction_id, name in cr.fetchall():
        cr.execute(
            "UPDATE tier_correction SET document_domain = %s WHERE id = %s",
            (str([("display_name", "ilike", name)]), correction_id),
        )
    cr.execute("ALTER TABLE tier_correction DROP COLUMN search_name")
