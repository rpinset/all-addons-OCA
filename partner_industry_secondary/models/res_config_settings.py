# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# Copyright 2025 Moduon - Eduardo de Miguel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_use_partner_industry_for_person = fields.Boolean(
        string="Use industry for individuals",
        help="Set if you want to be able to use industries for individuals also.",
        implied_group="partner_industry_secondary.group_use_partner_industry_for_person",
    )
    display_last_child_first = fields.Boolean(
        string="Display Child Industries first",
        help="Set if you want to show the last child industries first "
        "when displaying industries.\nChild (Parent < Grandparent)",
        config_parameter="partner_industry_secondary.display_last_child_first",
    )
