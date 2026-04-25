{
    "name": "Markdown Viewer Locale",
    "version": "18.0.3.0.4",
    "license": "LGPL-3",
    "category": "Tools",
    "summary": "View localized Markdown files based on user language",
    "author": "Rosen Vladimirov,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "depends": ["web"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "markdown_viewer_locale/static/src/lib/marked.min.js",
            "markdown_viewer_locale/static/src/lib/highlight.min.js",
            "markdown_viewer_locale/static/src/css/markdown_popup.css",
            (
                "after",
                "web/static/src/views/form/form_controller.xml",
                "markdown_viewer_locale/static/src/xml/form_controller.xml",
            ),
            "markdown_viewer_locale/static/src/js/markdown_registry.js",
            (
                "after",
                "web/static/src/views/form/form_controller.js",
                "markdown_viewer_locale/static/src/js/markdown_popup.js",
            ),
        ]
    },
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": False,
    "maintainers": ["rosenvladimirov"],
}
