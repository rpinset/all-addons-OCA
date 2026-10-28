import base64
import hashlib

from odoo import fields, models
from odoo.fields import Command


class ShopifyProductTemplate(models.Model):
    _inherit = "shopify.product.template"

    image_binding_ids = fields.One2many(
        "shopify.product.image",
        "template_binding_id",
        string="Shopify Images",
    )

    def _tracked_image_ids(self, binding):
        return super()._tracked_image_ids(binding) | set(
            binding.image_binding_ids.mapped("shopify_id")
        )

    def _has_image_drift(self, binding, product):
        incoming_ids = {image["id"] for image in product["images"] if image["id"]}
        return super()._has_image_drift(
            binding, product
        ) or incoming_ids != self._tracked_image_ids(binding)

    def _clear_image_bindings(self, binding):
        result = super()._clear_image_bindings(binding)
        binding.image_binding_ids.mapped("odoo_id").with_context(
            skip_shopify_export=True
        ).unlink()
        return result

    def _sync_extra_images(self, template_binding, images, variants, *, prune):
        result = super()._sync_extra_images(
            template_binding, images, variants, prune=prune
        )
        imported_ids = {image["id"] for image in images if image.get("id")}
        variants_by_media = {}
        bindings_by_gid = {
            item.shopify_id: item for item in template_binding.variant_binding_ids
        }
        for variant in variants:
            variant_binding = bindings_by_gid.get(variant["id"])
            if variant_binding:
                for media_id in variant["media_ids"]:
                    variants_by_media.setdefault(
                        media_id, self.env["shopify.product.variant"]
                    )
                    variants_by_media[media_id] |= variant_binding
        for position, payload in enumerate(images, start=1):
            if not payload["id"] or not payload["url"]:
                continue
            image_binding = self.env["shopify.product.image"].search(
                [
                    ("instance_id", "=", template_binding.instance_id.id),
                    ("shopify_id", "=", payload["id"]),
                ],
                limit=1,
            )
            image_bytes = self._download_image(payload["url"])
            checksum = hashlib.sha256(image_bytes).hexdigest()
            image_values = {
                "name": payload["alt"]
                or self.env._(
                    "%(product)s image %(position)s",
                    product=template_binding.odoo_id.name,
                    position=position,
                ),
                "image_1920": base64.b64encode(image_bytes),
                "sequence": position * 10,
            }
            variant_bindings = variants_by_media.get(
                payload["id"], self.env["shopify.product.variant"]
            )
            variant_binding = variant_bindings[:1]
            if len(variant_bindings) == 1:
                image_values["product_variant_id"] = variant_binding.odoo_id.id
                image_values["product_tmpl_id"] = False
            else:
                image_values["product_tmpl_id"] = template_binding.odoo_id.id
                image_values["product_variant_id"] = False
            if image_binding:
                image_binding.odoo_id.with_context(skip_shopify_export=True).write(
                    image_values
                )
                image_binding.write(
                    {
                        "source_url": payload["url"],
                        "image_checksum": checksum,
                        "variant_binding_id": variant_binding.id
                        if variant_binding
                        else False,
                        "variant_binding_ids": [Command.set(variant_bindings.ids)],
                        "state": "synced",
                        "error_message": False,
                        "last_sync_date": fields.Datetime.now(),
                    }
                )
            else:
                image = (
                    self.env["product.image"]
                    .with_context(skip_shopify_export=True)
                    .create(image_values)
                )
                self.env["shopify.product.image"].create(
                    {
                        "instance_id": template_binding.instance_id.id,
                        "shopify_id": payload["id"],
                        "template_binding_id": template_binding.id,
                        "variant_binding_id": variant_binding.id
                        if variant_binding
                        else False,
                        "variant_binding_ids": [Command.set(variant_bindings.ids)],
                        "odoo_id": image.id,
                        "source_url": payload["url"],
                        "image_checksum": checksum,
                        "state": "synced",
                        "last_sync_date": fields.Datetime.now(),
                    }
                )
        if prune:
            stale_bindings = template_binding.image_binding_ids.filtered(
                lambda item: item.shopify_id not in imported_ids
            )
            stale_bindings.mapped("odoo_id").with_context(
                skip_shopify_export=True
            ).unlink()
        return result

    def _product_extra_files(
        self, instance, template, binding, variants, existing_media_by_alt, base_url
    ):
        files, targets = super()._product_extra_files(
            instance, template, binding, variants, existing_media_by_alt, base_url
        )
        image_bindings = (
            {item.odoo_id.id: item for item in binding.image_binding_ids}
            if binding
            else {}
        )
        extra_images = (
            template.product_template_image_ids | variants.product_variant_image_ids
        )
        for image in extra_images:
            if not image.image_1920:
                continue
            checksum = self._binary_checksum(image.image_1920)
            image_binding = image_bindings.get(image.id)
            media_id = image_binding.shopify_id if image_binding else False
            unchanged = image_binding and image_binding.image_checksum == checksum
            export_alt = self._export_image_alt(image.name, image, checksum)
            matched_media_id = (
                media_id
                if media_id and unchanged
                else existing_media_by_alt.get(export_alt)
            )
            files.append(
                {"id": matched_media_id}
                if matched_media_id
                else {
                    "originalSource": self._public_image_url(
                        base_url, instance, image, checksum
                    ),
                    "alt": export_alt,
                }
            )
            targets.append(
                {
                    "kind": "extra",
                    "record": image,
                    "variant_id": image.product_variant_id.id,
                    "variant_ids": (
                        image_binding.variant_binding_ids.odoo_id.ids
                        if image_binding and image_binding.variant_binding_ids
                        else image.product_variant_id.ids
                    ),
                    "checksum": checksum,
                    "media_id": matched_media_id,
                    "alt": export_alt,
                }
            )
        return files, targets

    def _unmanaged_shopify_image_ids(self, binding, existing_media):
        # No super(): Odoo manages every image here, so images deleted in
        # Odoo must also be removed from Shopify.
        return []

    def _update_extra_image_binding(self, instance, binding, target, payload):
        result = super()._update_extra_image_binding(instance, binding, target, payload)
        target_variant_bindings = binding.variant_binding_ids.filtered(
            lambda item, target=target: (
                item.odoo_id.id in target.get("variant_ids", [])
            )
        )
        image_binding = self.env["shopify.product.image"].search(
            [
                ("instance_id", "=", instance.id),
                ("odoo_id", "=", target["record"].id),
            ],
            limit=1,
        )
        image_values = {
            "shopify_id": payload["id"],
            "template_binding_id": binding.id,
            "odoo_id": target["record"].id,
            "source_url": payload["url"],
            "image_checksum": target["checksum"],
            "variant_binding_id": target_variant_bindings[:1].id,
            "variant_binding_ids": [Command.set(target_variant_bindings.ids)],
            "state": "synced",
            "error_message": False,
            "last_sync_date": fields.Datetime.now(),
        }
        if image_binding:
            image_binding.write(image_values)
        else:
            self.env["shopify.product.image"].create(
                {
                    **image_values,
                    "instance_id": instance.id,
                }
            )
        return result
