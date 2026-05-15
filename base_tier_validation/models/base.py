from odoo import api, models


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def get_tier_review_action(self):
        """
        To be overridden for custom per-model action customization
        e.g. in `account.move` model class:

        @api.model
        def get_tier_review_action(self)
            action = self.env["ir.actions.actions"]._for_xml_id(
                "account.action_move_journal_line"
            )
            return action
        """
        return False
