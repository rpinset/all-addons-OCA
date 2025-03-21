# Copyright 2025 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """Update displayed names of departments, to be multi-language."""
    env["res.partner.department"].search([])._compute_display_name()
