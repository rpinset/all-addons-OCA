import base64
from unittest.mock import patch

from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector.tests.common import (
    MAIN_IMAGE_ID,
    SHARED_IMAGE_ID,
    VARIANT_IMAGE_ID,
    download_test_image,
    image_product_payload,
    png_bytes,
)


class TestShopifyExtraProductMedia(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = cls.env["shopify.instance"].create(
            {
                "name": "Media Shop",
                "shop_url": "media-shop.myshopify.com",
                "access_token": "test-token",
                "webhook_secret": "test-secret",
            }
        )
        cls.instance.state = "connected"
        cls.binding_model = cls.env["shopify.product.template"]

    def _import(self):
        with patch.object(
            type(self.binding_model),
            "_download_image",
            side_effect=download_test_image,
        ):
            return self.binding_model.browse(
                self.binding_model._job_import_product(
                    self.instance.id, image_product_payload(), payload_normalized=True
                )
            )

    def test_extra_media_only_keep_images_without_main_or_variant_role(self):
        binding = self._import()

        self.assertEqual(binding.state, "synced")
        self.assertEqual(
            binding.image_binding_ids.mapped("shopify_id"), [SHARED_IMAGE_ID]
        )
        self.assertEqual(
            binding.image_binding_ids.odoo_id.product_tmpl_id, binding.odoo_id
        )
        self.assertEqual(
            binding.image_binding_ids.variant_binding_ids,
            binding.variant_binding_ids,
        )
        self.assertEqual(
            self.binding_model._tracked_image_ids(binding),
            {MAIN_IMAGE_ID, VARIANT_IMAGE_ID, SHARED_IMAGE_ID},
        )
        self.assertFalse(self.binding_model._unmanaged_shopify_image_ids(binding, []))

    def test_reimport_removes_main_image_from_extra_media(self):
        binding = self._import()
        extra_main = self.env["product.image"].create(
            {
                "name": "Main image as extra media",
                "image_1920": base64.b64encode(png_bytes("red")),
                "product_tmpl_id": binding.odoo_id.id,
            }
        )
        self.env["shopify.product.image"].create(
            {
                "instance_id": self.instance.id,
                "shopify_id": MAIN_IMAGE_ID,
                "template_binding_id": binding.id,
                "odoo_id": extra_main.id,
            }
        )
        self.instance.field_mapping_ids.filtered(
            lambda mapping: mapping.field == "images"
        ).owner = "shopify"

        self._import()

        self.assertFalse(extra_main.exists())
        self.assertEqual(
            binding.image_binding_ids.mapped("shopify_id"), [SHARED_IMAGE_ID]
        )
