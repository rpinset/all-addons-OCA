# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import http
from odoo.http import request


class StorageFileController(http.Controller):
    @http.route(
        ["/storage.file/<string:slug_name_with_id>"], type="http", auth="public"
    )
    def content_common(self, slug_name_with_id, token=None, download=None, **kw):
        storage_file = request.env["storage.file"].get_from_slug_name_with_id(
            slug_name_with_id
        )
        stream = request.env["ir.binary"]._get_stream_from(
            storage_file, field_name="data"
        )
        return stream.get_response()
