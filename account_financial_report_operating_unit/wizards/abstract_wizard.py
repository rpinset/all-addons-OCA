# Copyright 2025 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AbstractWizard(models.AbstractModel):
    _inherit = "account_financial_report_abstract_wizard"

    operating_unit_ids = fields.Many2many(
        comodel_name="operating.unit",
    )

    def _prepare_report_data(self):
        res = super()._prepare_report_data()
        res.update({"operating_unit_ids": self.operating_unit_ids.ids or []})
        return res
