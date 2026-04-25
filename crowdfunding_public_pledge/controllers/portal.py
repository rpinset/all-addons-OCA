# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


from odoo import http

from odoo.addons.account.controllers import portal


class Portal(portal.PortalAccount):
    @http.route(
        ["/my/invoices/<int:invoice_id>/crowdfunding/public"],
        type="json",
        auth="public",
        website=True,
    )
    def set_public(self, invoice_id, access_token, is_public):
        invoice = self._document_check_access("account.move", invoice_id, access_token)
        invoice.crowdfunding_public = is_public
