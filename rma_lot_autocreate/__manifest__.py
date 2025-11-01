# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Rma Lot Autocreate",
    "summary": """Auto-generate stock lot at RMA confirm using per-operation sequence""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/rma",
    "depends": ["rma_lot", "product_expiry"],
    "maintainers": ["sbejaoui"],
    "data": ["views/rma_operation.xml", "data/ir_sequence_data.xml"],
    "demo": [],
}
