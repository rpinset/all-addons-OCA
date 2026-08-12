# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class EDIExchangePOGenerate(models.AbstractModel):
    """Generate purchase orders."""

    _description = "UBL output generator for purchase orders"

    _name = "edi.output.ubl.purchase.order"
    _inherit = "edi.oca.handler.generate"

    def generate(self, exchange_record):
        return self._generate_ubl_xml(exchange_record)

    def _generate_ubl_xml(self, exchange_record):
        order = exchange_record.record
        doc_type = order.get_ubl_purchase_order_doc_type()
        if not doc_type:
            raise NotImplementedError("TODO: handle no doc type")
        version = order.get_ubl_version()
        xml_string = order.generate_ubl_xml_string(doc_type, version=version)
        return xml_string
