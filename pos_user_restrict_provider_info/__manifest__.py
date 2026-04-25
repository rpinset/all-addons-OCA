{
    "name": "POS - Restrict Provider Info",
    "version": "18.0.1.0.0",
    "summary": "Restrict provider info to pos users",
    "category": "Point of Sale",
    "author": "ASPL-Nagarro, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/pos",
    "maintainers": ["BernatObrador"],
    "depends": ["point_of_sale"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_user_restrict_provider_info/static/src/**/*",
        ],
        "web.assets_tests": [
            "pos_user_restrict_provider_info/static/tests/tours/**/*",
        ],
    },
}
