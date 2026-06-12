{
    "name": "Mail Template Domain",
    "summary": "Filter mail templates by domain on the active record",
    "version": "18.0.1.0.0",
    "category": "Technical",
    "website": "https://github.com/OCA/mail",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["mail"],
    "data": [
        "views/mail_template_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mail_template_domain/static/src/js/*.js",
        ],
    },
}
