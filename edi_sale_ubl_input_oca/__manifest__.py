# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "EDI Sales",
    "summary": """
        Configuration and special behaviors for EDI on sales.
    """,
    "version": "14.0.1.1.0",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/edi",
    "depends": [
        "sale_order_import_ubl",
        "edi_sale_input_oca",
        "edi_sale_ubl_oca",
        "edi_ubl_oca",
        "edi_xml_oca",
    ],
    "data": [],
    "demo": [
        "demo/edi_exchange_type.xml",
    ],
}
