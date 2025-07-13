# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Mail suggested recipient unchecked",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/server-ux",
    "version": "17.0.1.0.0",
    "depends": ["mail"],
    "license": "AGPL-3",
    "category": "Tools",
    "installable": True,
    "maintainers": ["victoralmau"],
    "assets": {
        "web.assets_backend": [
            (
                "after",
                "mail/static/src/core/web/thread_service_patch.js",
                "mail_suggested_recipient_unchecked/static/src/js/thread_service_patch.esm.js",
            ),
        ],
    },
}
