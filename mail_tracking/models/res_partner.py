# Copyright 2016 Antonio Espinosa - <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "mail.bounced.mixin"]

    # tracking_emails_count and email_score are non-store fields in order
    # to improve performance
    tracking_emails_count = fields.Integer(
        compute="_compute_email_score_and_count", readonly=True
    )
    email_score = fields.Float(
        compute="_compute_email_score_and_count",
        search="_search_email_score",
    )

    def _search_email_score(self, operator, value):
        supported_operators = ["<", ">", "<=", ">=", "=", "!="]
        if operator not in supported_operators:
            raise NotImplementedError()
        weights = self.env["mail.tracking.email"]._email_score_weights()
        case_expr = " ".join(
            f"WHEN '{state}' THEN {score}" for state, score in weights.items()
        )
        state_expr = f"CASE state {case_expr} ELSE 0.0 END"
        query = f"""
            SELECT partner.id
            FROM res_partner partner
            LEFT JOIN (
                SELECT recipient_address,
                GREATEST(0.0, LEAST(100.0,
                    50.0 + SUM({state_expr})
                )) AS score
                FROM mail_tracking_email
                WHERE recipient_address IS NOT NULL
                GROUP BY recipient_address
            ) mte ON mte.recipient_address = LOWER(partner.email)
            WHERE COALESCE(mte.score, 50.0) {operator} %s
        """
        self.env.cr.execute(query, (value,))
        partner_ids = [row[0] for row in self.env.cr.fetchall()]
        return [("id", "in", partner_ids)]

    @api.depends("email")
    def _compute_email_score_and_count(self):
        self.email_score = 50.0
        self.tracking_emails_count = 0
        partners_mail = self.filtered("email")
        mt_obj = self.env["mail.tracking.email"].sudo()
        for partner in partners_mail:
            partner.email_score = mt_obj.email_score_from_email(partner.email)
            # We don't want performance issues due to heavy ACLs check for large
            # recordsets. Our option is to hide the number for regular users.
            if not self.env.user.has_group("base.group_system"):
                continue
            partner.tracking_emails_count = len(
                mt_obj._search([("recipient_address", "=", partner.email.lower())])
            )
