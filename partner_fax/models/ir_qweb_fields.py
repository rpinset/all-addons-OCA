# Copyright 2024 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models


class Contact(models.AbstractModel):
    _inherit = "ir.qweb.field.contact"

    @api.model
    def get_available_options(self):
        options = super().get_available_options()
        options["fields"]["params"]["params"].append(
            {
                "field_name": "fax",
                "label": _("Fax"),
            }
        )
        return options
