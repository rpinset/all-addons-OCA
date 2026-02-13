# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Rma Batch",
    "summary": """Group RMAs into batches for collective management""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/rma",
    "depends": ["rma"],
    "data": [
        "data/ir_sequence.xml",
        "security/rma_batch.xml",
        "views/rma.xml",
        "views/rma_batch.xml",
    ],
    "demo": [],
}
