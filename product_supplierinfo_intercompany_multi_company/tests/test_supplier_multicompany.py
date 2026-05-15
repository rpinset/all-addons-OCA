from odoo.addons.product_supplierinfo_intercompany.tests.test_supplier_intercompany import (
    TestIntercompanySupplierCase,
)


class TestSupplierMultiCompany(TestIntercompanySupplierCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other_company = cls.env["res.company"].create({"name": "Other company"})

    def test_supplier_all_companies(self):
        """
        Product and supplierinfo belongs to all companies
        """
        price = 5
        self.product_template_4.company_ids = False
        self._add_item(self.product_template_4, price)

        prod_with_other_company = self.product_template_4.with_company(
            self.other_company
        )
        self._check_supplier_info_for(self.product_template_4, price)
        self._check_supplier_info_for(prod_with_other_company, price)

        supplierinfo = self._get_supplier_info(self.product_template_4)
        self.assertFalse(supplierinfo.company_ids)

    def test_supplier_some_companies(self):
        """
        Product and supplierinfo belong only to two companies,
        not available to the third
        """
        price = 5
        companies = self.sale_company + self.purchase_company
        self.product_template_4.company_ids = companies
        self._add_item(self.product_template_4, price)

        # cannot use utility function _get_supplier_info
        # because company_id is hardcoded False
        # search from sale_company
        user = self.env.ref("base.user_admin")
        self.env = self.env(user=user)
        supplierinfo_model = self.env["product.supplierinfo"]
        user.write(
            {
                "company_id": self.sale_company.id,
                "company_ids": [(6, 0, self.sale_company.ids)],
            }
        )
        domain = [
            ("name", "=", self.partner.id),
            ("intercompany_pricelist_id", "=", self.pricelist_intercompany.id),
            ("product_tmpl_id", "=", self.product_template_4.id),
            ("product_id", "=", False),
        ]
        supplierinfo = supplierinfo_model.search(domain)
        self.assertEqual(supplierinfo.company_ids, companies)

        # run search again with other company
        user.write(
            {
                "company_id": self.other_company.id,
                "company_ids": [(6, 0, self.other_company.ids)],
            }
        )
        supplierinfo.invalidate_cache()
        supplierinfo = supplierinfo_model.search(domain)
        self.assertFalse(supplierinfo)

    def test_uninstall(self):
        from ..hooks import uninstall_hook

        uninstall_hook(self.env.cr, None)
        rule = self.env.ref("product.product_supplierinfo_comp_rule")
        domain = (
            " ['|', ('company_id', '=', user.company_id.id), "
            "('company_id', '=', False)]"
        )
        self.assertEqual(rule.domain_force, domain)
