# Hand the extra product media records over to the glue module
# shopify_connector_website_sale so that the upgrade does not delete them.
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    cr.execute(
        "SELECT id FROM ir_module_module WHERE name = %s",
        ["shopify_connector_website_sale"],
    )
    row = cr.fetchone()
    if not row:
        # Without the glue module the upgrade would delete these records.
        cr.execute("SELECT 1 FROM shopify_product_image LIMIT 1")
        if cr.fetchone():
            raise RuntimeError(
                "Add shopify_connector_website_sale to the addons path before "
                "upgrading shopify_connector, otherwise the Shopify extra "
                "product media bindings would be deleted."
            )
        _logger.warning(
            "shopify_connector_website_sale is not available: the empty "
            "shopify.product.image model will be removed."
        )
        return
    glue_id = row[0]
    # Move the XML IDs, except the constraint of the binding mixin.
    cr.execute(
        """
        UPDATE ir_model_data
        SET module = %s
        WHERE module = 'shopify_connector'
            AND (name LIKE %s OR name LIKE %s OR name IN %s)
            AND name != %s
        """,
        [
            "shopify_connector_website_sale",
            "%shopify\\_product\\_image%",
            "field\\_product\\_image\\_\\_%",
            (
                "model_product_image",
                "field_shopify_product_template__image_binding_ids",
            ),
            "constraint_shopify_product_image_instance_gid_unique",
        ],
    )
    # Move the table constraints, except the two of the binding mixin.
    cr.execute(
        """
        UPDATE ir_model_constraint
        SET module = %s
        WHERE model = (SELECT id FROM ir_model WHERE model = 'shopify.product.image')
            AND name NOT IN %s
        """,
        [
            glue_id,
            (
                "shopify_product_image_instance_gid_unique",
                "shopify_product_image_instance_id_fkey",
            ),
        ],
    )
    # Move the many2many table with the variant bindings.
    cr.execute(
        """
        UPDATE ir_model_relation
        SET module = %s
        WHERE model = (SELECT id FROM ir_model WHERE model = 'shopify.product.image')
        """,
        [glue_id],
    )
    # Install the glue module in this same upgrade.
    cr.execute(
        """
        UPDATE ir_module_module
        SET state = 'to install'
        WHERE id = %s AND state = 'uninstalled'
        """,
        [glue_id],
    )
