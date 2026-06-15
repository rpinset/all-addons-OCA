from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    ticket_active = fields.Boolean("Available for Helpdesk Tickets", default=True)
    helpdesk_ticket_ids = fields.One2many(
        related="product_variant_ids.helpdesk_ticket_ids"
    )
    helpdesk_ticket_count = fields.Integer(compute="_compute_helpdesk_ticket_count")

    @api.depends("helpdesk_ticket_ids")
    def _compute_helpdesk_ticket_count(self):
        for template in self:
            template.helpdesk_ticket_count = len(template.helpdesk_ticket_ids)

    def action_view_helpdesk_tickets(self, product=None):
        product = product or self
        product.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "helpdesk_mgmt.helpdesk_ticket_action"
        )
        if product.helpdesk_ticket_count <= 1:
            ticket = product.helpdesk_ticket_ids
            product_id = False
            if product.is_product_variant or len(product.product_variant_ids) == 1:
                product_id = product.product_variant_id.id
            action.update(
                {
                    "res_id": ticket.id,
                    "views": [(False, "form")],
                    "context": {"default_product_id": product_id},
                }
            )
        else:
            action.update(
                {
                    "domain": [("id", "in", product.helpdesk_ticket_ids.ids)],
                }
            )
        return action


class ProductProduct(models.Model):
    _inherit = "product.product"

    helpdesk_ticket_ids = fields.One2many(
        comodel_name="helpdesk.ticket", inverse_name="product_id"
    )
    helpdesk_ticket_count = fields.Integer(compute="_compute_helpdesk_ticket_count")

    @api.depends("helpdesk_ticket_ids")
    def _compute_helpdesk_ticket_count(self):
        for template in self:
            template.helpdesk_ticket_count = len(template.helpdesk_ticket_ids)

    def action_view_helpdesk_tickets(self):
        self.ensure_one()
        return self.product_tmpl_id.action_view_helpdesk_tickets(product=self)
