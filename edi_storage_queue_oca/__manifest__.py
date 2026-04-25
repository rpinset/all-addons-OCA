# Copyright 2020 ACSONE
# Copyright 2025 Dixmit
# @author: Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "EDI Storage integration with Queue",
    "summary": """
    Integrates EDI Storage with Queue
    """,
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/edi-framework",
    "author": "ACSONE,Odoo Community Association (OCA)",
    "depends": ["edi_storage_oca", "edi_queue_oca"],
    "data": [
        "data/job_channel_data.xml",
        "data/queue_job_function_data.xml",
    ],
}
