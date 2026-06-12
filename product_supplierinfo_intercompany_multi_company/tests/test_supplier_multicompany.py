from odoo.addons.product_supplierinfo_intercompany.tests.test_supplier_intercompany import (
    TestIntercompanySupplierCase,
)


class TestSupplierMultiCompany(TestIntercompanySupplierCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other_company = cls.env["res.company"].create({"name": "Other company"})
        cls.product_template_3 = cls.env.ref(
            "product.product_product_3_product_template"
        )

    def test_supplier_all_companies(self):
        """
        Product and supplierinfo belongs to all companies
        """
        product = self.product_template_3
        self._check_no_supplier_info_for(product)
        price = 5
        product.company_ids = False
        self._add_item(product, price)

        # Search and compare manually instead of using
        # _get_supplier info/_check_supplier_info_for
        # compat with product_supplierinfo_group
        domain = [
            ("name", "=", self.partner.id),
            ("intercompany_pricelist_id", "=", self.pricelist_intercompany.id),
            ("product_tmpl_id", "=", product.id),
            ("product_id", "=", False),
        ]
        supplierinfo = self.env["product.supplierinfo"].search(domain)
        self.assertEqual(len(supplierinfo), 1)
        self.assertEqual(supplierinfo.price, price)
        self.assertEqual(
            supplierinfo.currency_id, supplierinfo.intercompany_pricelist_id.currency_id
        )
        self.assertFalse(supplierinfo.company_ids)

        product.with_company(self.other_company)
        supplierinfo_other_company = (
            self.env["product.supplierinfo"]
            .with_company(self.other_company)
            .search(domain)
        )
        self.assertEqual(supplierinfo, supplierinfo_other_company)

    def test_supplier_some_companies(self):
        """
        Product and supplierinfo belong only to two companies,
        not available to the third
        """
        product = self.product_template_3
        self._check_no_supplier_info_for(product)
        price = 5
        companies = self.sale_company + self.purchase_company
        product.company_ids = companies
        self._add_item(product, price)

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
            ("product_tmpl_id", "=", product.id),
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
