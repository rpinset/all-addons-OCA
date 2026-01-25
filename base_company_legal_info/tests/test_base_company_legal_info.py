# © 2014-2016 Akretion (http://www.akretion.com)
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestBaseCompanyLegalInfo(TransactionCase):
    def setUp(self):
        super().setUp()
        self.company_grap = self.env.ref("base_company_legal_info.company_grap")

    def test_01_compute_report_legal_description(self):
        self.company_grap._compute_report_legal_description()
        self.assertEqual(
            self.company_grap.report_legal_description,
            "GRAP, Groupement Régional Alimentaire de Proximité, SA coopérative à "
            "conseil d'administration",
        )

        # Test without legal_name
        self.company_grap.legal_name = False
        self.company_grap._compute_report_legal_description()
        self.assertEqual(
            self.company_grap.report_legal_description,
            "GRAP, SA coopérative à conseil d'administration",
        )

        # Test without legal_type
        self.company_grap.legal_type = False
        self.company_grap._compute_report_legal_description()
        self.assertEqual(self.company_grap.report_legal_description, "GRAP")
