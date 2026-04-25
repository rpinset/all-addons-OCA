# Copyright 2022 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Pos Vat Tree",
    "summary": """Point of Sale: Show VAT number at Customer Tree View""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "KMEE,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/pos",
    "maintainers": ["mileo"],
    "depends": [
        "point_of_sale",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            (
                "after",
                "point_of_sale/static/src/app/screens/partner_list/partner_line/partner_line.xml",
                "pos_customer_tree_view_vat/static/src/xml/partner_line.xml",
            ),
            (
                "after",
                "point_of_sale/static/src/app/screens/partner_list/partner_list.xml",
                "pos_customer_tree_view_vat/static/src/xml/partner_list_screen.xml",
            ),
        ],
    },
}
