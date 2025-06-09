# Copyright 2022 Camptocamp SA
# @author: Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import os
import random

from odoo.addons.sale_order_import_ubl.tests.common import get_test_data


def get_xml_handler(backend, schema_path, model=None):
    model = model or backend._name
    return backend._find_component(
        model,
        ["edi.xml"],
        work_ctx={"schema_path": schema_path},
        safe=False,
    )


def flatten(txt):
    return "".join([x.strip() for x in txt.splitlines()])


def dev_write_example_file(filename, content, test_file=None):
    test_file = test_file or __file__
    from pathlib import Path

    path = Path(test_file).parent / ("examples/test." + filename)
    with open(path, "w") as out:
        out.write(content)


def read_test_file(filename):
    path = os.path.join(os.path.dirname(__file__), "examples", filename)
    with open(path, "r") as thefile:
        return thefile.read()


class OrderInboundTestMixin:
    @classmethod
    def _setup_inbound_record(cls, backend, type_in):
        cls.exc_type_in = type_in
        cls.exc_type_in.backend_id = backend
        cls.exc_record_in = backend.create_record(
            cls.exc_type_in.code, {"edi_exchange_state": "input_received"}
        )

    @classmethod
    def _setup_inbound_order(cls, backend, type_in):
        cls._setup_inbound_record(backend, type_in)
        cls.ubl_data = get_test_data(cls.env)
        # Ensure all products have a barcode
        for data in cls.ubl_data.values():
            for prod in data.products:
                prod.barcode = prod.id * 14
        cls.client_order_ref = str(random.randint(1000, 9999))
        fname = "UBL-Order-2.1-Example.xml"
        cls.ubl_data[fname]["client_order_ref"] = cls.client_order_ref
        cls.order_data = cls.ubl_data[fname]
        fcontent = cls.order_data._get_content().decode()
        fcontent = fcontent.replace(
            "<cbc:ID>34</cbc:ID>", f"<cbc:ID>{cls.client_order_ref}</cbc:ID>"
        )
        cls.exc_record_in._set_file_content(fcontent)
        cls.err_msg_already_imported = "Sales order has already been imported before"

    def _find_order(self):
        return self.env["sale.order"].search(
            [
                ("client_order_ref", "=", self.client_order_ref),
                ("commercial_partner_id", "=", self.order_data.partner.parent_id.id),
            ]
        )
