# © 2017 Raphael REVERDY <raphael.reverdy@akretion.com>
#        David BEAL <david.beal@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Delivery Carrier La Poste (fr)",
    "version": "16.0.1.1.0",
    "summary": "Generate Label for La Poste/Colissimo",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainers": ["florian-dacosta"],
    "website": "https://github.com/OCA/delivery-carrier",
    "category": "Warehouse",
    "depends": [
        "partner_address_split",
        "delivery_roulier_option",
        "intrastat_base",  # for customs declaration
    ],
    "data": [
        "data/delivery.xml",
        "views/carrier_account_views.xml",
        "views/stock_picking.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
