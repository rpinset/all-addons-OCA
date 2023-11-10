from odoo import fields, models


class Nkd(models.Model):
    _name = "l10n.hr.nkd"
    _description = "HR NKD - national occupational calssification"

    code = fields.Char(size=16, required=True)
    name = fields.Char(required=True)

    def name_get(self):
        res = [((c.id, "%s - %s" % (c.code, c.name))) for c in self]
        return res
