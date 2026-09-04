# Copyright 2015-2018 Tecnativa - Pedro M. Baeza
# Copyright 2021 Tecnativa - Jo??o Marques
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, exceptions, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    agent_type = fields.Selection(
        selection_add=[("salesman", "Salesman (employee)")],
    )

    @api.constrains("agent_type")
    def _check_employee(self):
        for partner in self:
            if partner.agent_type == "salesman" and not partner.employee:
                raise exceptions.ValidationError(
                    self.env._(
                        "There must one (and only one) employee linked to this "
                        "partner. To do this, go to 'Employees' and create an "
                        "Employee with a 'Related User' under 'HR Settings'."
                    )
                )
