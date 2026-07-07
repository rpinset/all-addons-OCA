# Copyright 2026 TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Field Service - Digitized Signature",
    "summary": "Capture a digitized signature on Field Service orders",
    "version": "16.0.1.0.0",
    "category": "Field Service",
    "license": "AGPL-3",
    "author": "TAKOBI, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/field-service",
    "depends": ["fieldservice"],
    "data": [
        "report/fsm_order_report_template.xml",
        "views/fsm_order.xml",
    ],
    "development_status": "Beta",
    "installable": True,
}
