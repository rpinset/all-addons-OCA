# Copyright 2020 Dixmit
# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "EDI WebService",
    "summary": """
        Defines webservice integration from EDI Exchange records""",
    "version": "18.0.2.0.0",
    "license": "AGPL-3",
    "development_status": "Beta",
    "author": "Dixmit, Camptocamp, Odoo Community Association (OCA)",
    "maintainers": ["etobella", "simahawk"],
    "website": "https://github.com/OCA/edi-framework",
    "depends": ["edi_webservice_core_oca", "edi_webservice_component_oca"],
    "post_load": "post_load_hook",
}
