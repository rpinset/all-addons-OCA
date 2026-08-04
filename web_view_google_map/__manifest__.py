# Copyright (C) 2019, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Google Map View",
    "summary": "Add a Google Map view type to the Odoo web client",
    "version": "19.0.1.0.2",
    "author": "Open Source Integrators, Gray Matter Logic, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/geospatial",
    "license": "AGPL-3",
    "category": "Extra Tools",
    "depends": ["base_google_map", "contacts"],
    "data": ["views/res_partner.xml"],
    "images": ["static/description/thumbnails.png"],
    "assets": {
        "web.assets_backend": [
            "web_view_google_map/static/lib/markerclusterer/markerclusterer.min.js",
            "web_view_google_map/static/src/views/google_map/map_themes.esm.js",
            "web_view_google_map/static/src/views/google_map/google_maps_loader.esm.js",
            "web_view_google_map/static/src/views/google_map/google_map_renderer.scss",
            "web_view_google_map/static/src/views/google_map/google_map_renderer.esm.js",
            "web_view_google_map/static/src/views/google_map/google_map_renderer.xml",
            "web_view_google_map/static/src/views/google_map/google_map_controller.esm.js",
            "web_view_google_map/static/src/views/google_map/google_map_controller.xml",
            "web_view_google_map/static/src/views/google_map/google_map_view.esm.js",
            "web_view_google_map/static/src/fields/gplaces_autocomplete.esm.js",
            "web_view_google_map/static/src/fields/gplaces_autocomplete.xml",
            "web_view_google_map/static/src/fields/gplaces_address_form.esm.js",
            "web_view_google_map/static/src/fields/gplaces_address_form.xml",
        ],
    },
    "installable": True,
    "uninstall_hook": "uninstall_hook",
    "maintainers": ["gityopie", "wolfhall"],
}
