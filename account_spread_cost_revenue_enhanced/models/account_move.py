from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    # To avoid recursion when creating a spread from a journal entry using templates
    is_created_from_spread = fields.Boolean(
        string="Created from Spread",
        default=False,
    )

    def action_post(self):
        """Use templates in journal entries too"""
        for move in self.filtered(
            lambda m: not m.is_created_from_spread and m.move_type == "entry"
        ):
            spread_autos = self.env["account.spread.template.auto"].search(
                [("template_id.auto_spread", "=", True)]
            )

            for line in move.line_ids:
                account = line.account_id
                matched_spreads = spread_autos.filtered(
                    lambda s, a=account: s.account_id == a
                )
                templates = matched_spreads.mapped("template_id")

                if not templates:
                    continue

                if len(templates) > 1:
                    raise UserError(
                        _(
                            "Too many auto spread templates (%(count)d) matched with account %(account)s."
                        )
                        % {"count": len(templates), "account": account.code}
                    )

                wizard = self.env["account.spread.invoice.line.link.wizard"].new(
                    {
                        "invoice_line_id": line.id,
                        "company_id": line.company_id.id,
                        "spread_action_type": "template",
                        "template_id": templates[0].id,
                    }
                )
                wizard.confirm()
        return super().action_post()
