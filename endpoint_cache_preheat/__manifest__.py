# Copyright 2025 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Endpoint cache pre-heat",
    "summary": """Provide basic pre-caching features for endpoints""",
    "version": "18.0.1.0.0",
    "license": "LGPL-3",
    "development_status": "Alpha",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "maintainers": ["simahawk"],
    "website": "https://github.com/OCA/web-api",
    "depends": ["endpoint_cache", "queue_job"],
    "data": [
        "views/endpoint_view.xml",
        "data/cron.xml",
        "data/job_channel.xml",
        "data/job_function.xml",
    ],
}
