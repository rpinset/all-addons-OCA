from odoo import api, fields, models


class ResBankCorrAcc(models.Model):
    _name = "res.bank.corracc"
    _description = "Correspondent accounts of Russian banks"
    _rec_name = "corr_acc"

    bank_id = fields.Many2one(comodel_name="res.bank", string="Bank")

    corr_acc = fields.Char(
        string="Correspondent account",
        help="Correspondent account used by Russian banks",
    )


class ResBank(models.Model):
    _inherit = "res.bank"
    _description = "Russian Banks"

    corr_acc_ids = fields.One2many(
        comodel_name="res.bank.corracc",
        inverse_name="bank_id",
        string="Correspondent accounts",
    )

    country_code = fields.Char(related="country.code", store=False)


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    @api.onchange("bank_id")
    def onchange_bank_id(self):
        self.bank_name = self.bank_id.name
        self.bank_bic = self.bank_id.bic
