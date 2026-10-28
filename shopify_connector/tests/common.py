import io

from PIL import Image

IMAGE_PRODUCT_ID = "gid://shopify/Product/700"
MAIN_IMAGE_ID = "gid://shopify/MediaImage/710"
VARIANT_IMAGE_ID = "gid://shopify/MediaImage/711"
SHARED_IMAGE_ID = "gid://shopify/MediaImage/712"
IMAGE_COLORS = {"710": "red", "711": "blue", "712": "green"}


def assert_shopify_models_have_company_rules(testcase):
    """Fail with all concrete Shopify models missing an ir.rule."""
    models = testcase.env["ir.model"].search([("model", "=like", "shopify.%")])
    missing = []
    for model in models:
        runtime = testcase.env.registry.get(model.model)
        if not runtime or runtime._abstract:
            continue
        if not testcase.env["ir.rule"].search_count(
            [("model_id", "=", model.id)], limit=1
        ):
            missing.append(model.model)
    testcase.assertFalse(
        missing,
        "Shopify models without a company record rule: " + ", ".join(sorted(missing)),
    )


def png_bytes(color):
    buffer = io.BytesIO()
    Image.new("RGB", (1, 1), color).save(buffer, format="PNG")
    return buffer.getvalue()


def download_test_image(url):
    return png_bytes(IMAGE_COLORS[url.rsplit("/", 1)[-1].split(".")[0]])


def image_product_payload():
    return {
        "id": IMAGE_PRODUCT_ID,
        "name": "Media Shirt",
        "description": "",
        "handle": "media-shirt",
        "status": "ACTIVE",
        "updated_at": "2026-10-20T00:00:00Z",
        "options": [
            {
                "id": "gid://shopify/ProductOption/70",
                "name": "Color",
                "position": 1,
                "values": ["Blue", "Red"],
            }
        ],
        "variants": [
            {
                "id": "gid://shopify/ProductVariant/701",
                "title": "Blue",
                "sku": "MEDIA-BLUE",
                "barcode": "",
                "price": "10.00",
                "selected_options": [{"name": "Color", "value": "Blue"}],
                "media_ids": [VARIANT_IMAGE_ID, SHARED_IMAGE_ID],
                "updated_at": "2026-10-20T00:00:00Z",
            },
            {
                "id": "gid://shopify/ProductVariant/702",
                "title": "Red",
                "sku": "MEDIA-RED",
                "barcode": "",
                "price": "10.00",
                "selected_options": [{"name": "Color", "value": "Red"}],
                "media_ids": [SHARED_IMAGE_ID],
                "updated_at": "2026-10-20T00:00:00Z",
            },
        ],
        "images": [
            {
                "id": image_id,
                "url": f"https://cdn.example.com/{image_id.rsplit('/', 1)[-1]}.png",
                "alt": "",
                "media_content_type": "IMAGE",
            }
            for image_id in (MAIN_IMAGE_ID, VARIANT_IMAGE_ID, SHARED_IMAGE_ID)
        ],
        "collections": [],
    }
