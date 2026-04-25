# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "EDI Sales UBL",
    "summary": """
        Configuration and special behaviors for EDI UBL exchanges related to sales.
    """,
    "version": "18.0.1.0.2",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/edi-framework",
    "depends": [
        "edi_sale_oca",
        "edi_state_oca",
        "edi_ubl_oca",
        # This could be made optional
        # but the delivery part would need another source of data
        "sale_stock",
    ],
    "data": [
        "data/edi_state.xml",
        "views/sale_order.xml",
    ],
    "demo": [
        "demo/edi_exchange_type.xml",
    ],
}
