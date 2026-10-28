from odoo.addons.shopify_connector.controllers import product_image


class ShopifyProductImageController(product_image.ShopifyProductImageController):
    def _image_models(self):
        return super()._image_models() | {"product.image"}

    def _image_template(self, record):
        if record._name == "product.image":
            return record.product_tmpl_id or record.product_variant_id.product_tmpl_id
        return super()._image_template(record)
