# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

_QUALITY_PARTNER_LOG = [
    ("3_good", "Good"),
    ("2_regular", "Regular"),
    ("1_bad", "Bad"),
]


class ResPartner(models.Model):
    _inherit = "res.partner"

    price_quality = fields.Selection(
        selection=_QUALITY_PARTNER_LOG,
        string="Value for money",
        default="2_regular",
        required=True,
    )
    service_quality = fields.Selection(
        selection=_QUALITY_PARTNER_LOG,
        string="Service",
        default="2_regular",
        required=True,
    )
    attention_quality = fields.Selection(
        selection=_QUALITY_PARTNER_LOG,
        string="Attention given",
        default="2_regular",
        required=True,
    )
    qualification_log_ids = fields.One2many(
        comodel_name="quality.partner.log",
        inverse_name="partner_id",
    )
    partner_quality = fields.Integer(
        compute="_compute_partner_quality",
    )
    qualification_date = fields.Date()

    @api.depends("price_quality", "service_quality", "attention_quality")
    def _compute_partner_quality(self):
        for partner in self:
            price = int(partner.price_quality[0])
            service = int(partner.service_quality[0])
            attention = int(partner.attention_quality[0])
            partner.partner_quality = price + service + attention
            partner.qualification_date = fields.Date.today()

    def _prepare_qualification_log_vals(self):
        self.ensure_one()
        return {
            "partner_id": self.id,
            "price_quality": self.price_quality,
            "service_quality": self.service_quality,
            "attention_quality": self.attention_quality,
            "partner_quality": self.partner_quality,
            "qualification_date": self.qualification_date,
        }

    def _update_qualification_log(self):
        Log = self.env["quality.partner.log"]
        self.ensure_one()
        Log.create(self._prepare_qualification_log_vals())

    def write(self, values):
        res = super().write(values)
        for partner in self:
            if (
                "price_quality" in values
                or "service_quality" in values
                or "attention_quality" in values
            ):
                partner._update_qualification_log()
        return res
