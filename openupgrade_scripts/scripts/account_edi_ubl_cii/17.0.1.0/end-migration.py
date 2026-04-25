# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def _res_partner_compute_fields_values(env):
    partners = (
        env["res.partner"]
        .with_context(active_test=False)
        .search(["|", ("country_id", "!=", False), ("vat", "!=", False)])
    )
    partners._compute_ubl_cii_format()
    partners._compute_peppol_eas()


@openupgrade.migrate()
def migrate(env, version):
    _res_partner_compute_fields_values(env)
