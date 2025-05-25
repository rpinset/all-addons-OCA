# Copyright 2017 ACSONE SA/NV
# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailTemplate(models.Model):

    _inherit = "mail.template"

    company_id = fields.Many2one(
        "res.company",
        ondelete="set null",
    )
    original_xmlid_mail_template_id = fields.Many2one(
        comodel_name="mail.template",
        string="Original XMLID template",
        help="Mail Template that corresponds to a record having a XMLID. "
        "This record will be used when the record having a XMLID is found "
        "but cannot be accessed.",
    )
    substitute_xmlid_mail_template_ids = fields.One2many(
        comodel_name="mail.template",
        inverse_name="original_xmlid_mail_template_id",
        string="Substitutes for XMLID template",
        help="Mail Templates that correspond to this record's XMLID. "
        "When this record is searched by XMLID but cannot be accessed, "
        "the first accessible substitute will be found instead.",
    )

    def copy(self, default=None):
        has_xmlid = self.get_external_id()[self.id]
        if has_xmlid:
            default = dict(default or {})
            default["original_xmlid_mail_template_id"] = self.id
        return super().copy(default=default)
