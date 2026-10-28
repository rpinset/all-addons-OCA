import base64
import hashlib

from werkzeug.wrappers import Response

from odoo import http
from odoo.http import request
from odoo.tools.mimetypes import guess_mimetype

from ..lib.product import verify_product_image_signature


class ShopifyProductImageController(http.Controller):
    @http.route(
        (
            "/shopify/product-image/<int:instance_id>/<string:model_name>/"
            "<int:record_id>/<string:checksum>/<string:signature>"
        ),
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
        save_session=False,
    )
    def shopify_product_image(
        self,
        instance_id,
        model_name,
        record_id,
        checksum,
        signature,
        **_kwargs,
    ):
        instance = request.env["shopify.instance"].sudo().browse(instance_id).exists()
        if (
            not instance
            or not instance.active
            or model_name not in self._image_models()
            or not verify_product_image_signature(
                signature,
                instance.webhook_secret,
                instance.id,
                model_name,
                record_id,
                checksum,
            )
        ):
            return Response(status=404)

        record = request.env[model_name].sudo().browse(record_id).exists()
        if not record or not self._record_company_matches(record, instance):
            return Response(status=404)
        encoded = record.image_1920
        if not encoded:
            return Response(status=404)
        raw = base64.b64decode(encoded)
        if hashlib.sha256(raw).hexdigest() != checksum:
            return Response(status=404)
        response = Response(
            raw,
            content_type=guess_mimetype(raw) or "application/octet-stream",
        )
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        return response

    def _image_models(self):
        return {"product.template", "product.product"}

    def _image_template(self, record):
        if record._name == "product.template":
            return record
        return record.product_tmpl_id

    def _record_company_matches(self, record, instance):
        template = self._image_template(record)
        return not template.company_id or template.company_id == instance.company_id
