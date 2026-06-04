# Copyright 2023 ForgeFlow S.L. (http://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "EDI Product",
    "summary": """
       EDI framework configuration and base logic
       for products and units of measure""",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/edi-framework",
    "depends": [
        # Odoo/core
        "product",
        # OCA/edi-framework
        # Replaced ``edi_endpoint_oca`` dependency with ``edi_core_oca``
        # For version 18.0 without ``edi_endpoint_oca``, CI fails
        # because ``origin_edi_endpoint_id`` is set up on product models
        # while its related target ``edi.exchange.record.edi_endpoint_id`` is absent.
        # A glue module similar to ``edi_sale_endpoint`` does not currently solve it.
        # "edi_endpoint_oca",
        "edi_core_oca",
    ],
    "data": [
        "views/product_views.xml",
        "views/uom_uom_views.xml",
    ],
}
