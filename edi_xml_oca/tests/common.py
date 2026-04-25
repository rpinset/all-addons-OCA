# Copyright 2020 ACSONE
# @author: Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import os

import xmlunittest

from odoo.addons.component.tests.common import TransactionComponentCase


class XMLTestCaseMixin(xmlunittest.XmlTestMixin):
    def _dev_write_example_file(self, test_file, filename, content):
        from pathlib import Path

        path = Path(test_file).parent / ("examples/test." + filename)
        with open(path, "w") as out:
            out.write(content)

    def flatten(self, txt):
        return "".join([x.strip() for x in txt.splitlines()])

    def read_test_file(self, filename):
        path = os.path.join(os.path.dirname(__file__), "examples", filename)
        with open(path) as thefile:
            return thefile.read()


class XMLComponentTestCase(TransactionComponentCase, XMLTestCaseMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend = cls.env.ref("edi_oca.demo_edi_backend")
        cls.handler = cls.backend._find_component(
            cls.backend._name,
            ["edi.xml"],
            work_ctx={"schema_path": "edi_xml_oca:tests/fixtures/Test.xsd"},
        )
