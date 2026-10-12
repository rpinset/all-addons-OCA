from datetime import date, timedelta

from odoo.tests.common import TransactionCase


class LibroCommonCase(TransactionCase):
    """Base fixture shared by the l10n_py_libros test suite."""

    # Período fixo, isolado das datas "hoje" usadas pelos dados demo de
    # l10n_py_account/l10n_py_edi_base (que poluiriam o domínio de
    # action_generate_lines caso o teste usasse a data corrente).
    TEST_YEAR = 2030
    TEST_MONTH = 6
    TEST_DATE = date(TEST_YEAR, TEST_MONTH, 15)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        cls.country_py = cls.env.ref("base.py")
        cls.company.write(
            {
                "country_id": cls.country_py.id,
                "account_fiscal_country_id": cls.country_py.id,
                "l10n_py_ruc": "80009401",
            }
        )
        # Self-sufficient fixture: a clean DB (e.g. OCA CI) has the generic
        # chart, which lacks the tax groups/accounts these tests rely on.
        if cls.company.chart_template != "py":
            cls.env["account.chart.template"].try_loading(
                "py", cls.company, install_demo=False
            )

        cls.doc_type_factura = cls.env.ref("l10n_py_account.dc_py_f")
        cls.doc_type_autofactura = cls.env.ref("l10n_py_account.dc_py_af")
        cls.doc_type_nc = cls.env.ref("l10n_py_account.dc_py_nc")
        cls.doc_type_nd = cls.env.ref("l10n_py_account.dc_py_nd")

        cls.account_income = cls.env["account.account"].search(
            [
                ("company_ids", "in", cls.company.id),
                ("account_type", "=", "income"),
            ],
            limit=1,
        )
        cls.account_expense = cls.env["account.account"].search(
            [
                ("company_ids", "in", cls.company.id),
                ("account_type", "=", "expense"),
            ],
            limit=1,
        )
        cls.account_receivable = cls.env["account.account"].search(
            [
                ("company_ids", "in", cls.company.id),
                ("account_type", "=", "asset_receivable"),
            ],
            limit=1,
        )
        cls.account_payable = cls.env["account.account"].search(
            [
                ("company_ids", "in", cls.company.id),
                ("account_type", "=", "liability_payable"),
            ],
            limit=1,
        )

        cls.sale_journal = cls.env["account.journal"].create(
            {
                "name": "Ventas Libros Test",
                "type": "sale",
                "code": "VLT",
                "company_id": cls.company.id,
                "l10n_latam_use_documents": True,
            }
        )
        cls.purchase_journal = cls.env["account.journal"].create(
            {
                "name": "Compras Libros Test",
                "type": "purchase",
                "code": "CLT",
                "company_id": cls.company.id,
                "l10n_latam_use_documents": True,
            }
        )

        today = date.today()
        cls.authorization = cls.env["account.authorization"].create(
            {
                "name": "19191919",
                "date_from": today - timedelta(days=30),
                "date_to": today + timedelta(days=335),
                "invoice_number_from": 1,
                "invoice_number_to": 100000,
                "establishment": "001",
                "expedition_point": "001",
                "l10n_latam_document_type_id": cls.doc_type_factura.id,
                "company_id": cls.company.id,
            }
        )
        cls.authorization_nc = cls.env["account.authorization"].create(
            {
                "name": "19191920",
                "date_from": today - timedelta(days=30),
                "date_to": today + timedelta(days=335),
                "invoice_number_from": 1,
                "invoice_number_to": 100000,
                "establishment": "001",
                "expedition_point": "001",
                "l10n_latam_document_type_id": cls.doc_type_nc.id,
                "company_id": cls.company.id,
            }
        )

        cls.customer = cls.env["res.partner"].create(
            {
                "name": "Cliente Libros Test",
                "country_id": cls.country_py.id,
                "l10n_py_ruc": "80011111",
                "l10n_py_taxpayer_type": "1",
            }
        )
        cls.supplier = cls.env["res.partner"].create(
            {
                "name": "Proveedor Libros Test",
                "country_id": cls.country_py.id,
                "l10n_py_ruc": "80022222",
                "l10n_py_taxpayer_type": "1",
            }
        )

        cls.tax_10 = cls.env["account.tax"].create(
            {
                "name": "IVA 10% Libros Test",
                "amount": 10.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "price_include_override": "tax_included",
            }
        )
        cls.tax_5 = cls.env["account.tax"].create(
            {
                "name": "IVA 5% Libros Test",
                "amount": 5.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "price_include_override": "tax_included",
            }
        )
        cls.tax_exempt = cls.env["account.tax"].create(
            {
                "name": "Exento Libros Test",
                "amount": 0.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
            }
        )
        cls.tax_exonerado = cls.env["account.tax"].create(
            {
                "name": "Exonerado Libros Test",
                "amount": 0.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "l10n_py_iva_affectation": "2",
            }
        )
        cls.tax_10_purchase = cls.env["account.tax"].create(
            {
                "name": "IVA 10% Compras Libros Test",
                "amount": 10.0,
                "amount_type": "percent",
                "type_tax_use": "purchase",
                "price_include_override": "tax_included",
            }
        )
        cls.tax_5_purchase = cls.env["account.tax"].create(
            {
                "name": "IVA 5% Compras Libros Test",
                "amount": 5.0,
                "amount_type": "percent",
                "type_tax_use": "purchase",
                "price_include_override": "tax_included",
            }
        )
        cls.tax_exempt_purchase = cls.env["account.tax"].create(
            {
                "name": "Exento Compras Libros Test",
                "amount": 0.0,
                "amount_type": "percent",
                "type_tax_use": "purchase",
            }
        )

        cls.product = cls.env["product.product"].create(
            {"name": "Producto Libros Test", "list_price": 1100.0}
        )
        line_model = cls.env["account.payment.term.line"]
        days_field = "nb_days" if "nb_days" in line_model._fields else "days"
        cls.term_credit = cls.env["account.payment.term"].create(
            {
                "name": "30 dias Libros Test",
                "line_ids": [
                    (0, 0, {days_field: 30, "value_amount": 100, "value": "percent"}),
                ],
            }
        )

    def _create_invoice(self, move_type, products_taxes, doc_type=None, **kwargs):
        lines = []
        account = (
            self.account_income
            if move_type in ("out_invoice", "out_refund")
            else self.account_expense
        )
        for product, tax, price in products_taxes:
            lines.append(
                (
                    0,
                    0,
                    {
                        "product_id": product.id,
                        "quantity": 1,
                        "price_unit": price,
                        "tax_ids": [(6, 0, [tax.id] if tax else [])],
                        "account_id": account.id,
                    },
                )
            )
        vals = {
            "move_type": move_type,
            "partner_id": (
                self.customer
                if move_type in ("out_invoice", "out_refund")
                else self.supplier
            ).id,
            "journal_id": (
                self.sale_journal
                if move_type in ("out_invoice", "out_refund")
                else self.purchase_journal
            ).id,
            "invoice_date": self.TEST_DATE,
            "invoice_line_ids": lines,
        }
        if doc_type:
            vals["l10n_latam_document_type_id"] = doc_type.id
        if (
            move_type in ("in_invoice", "in_refund")
            and "l10n_latam_document_number" not in kwargs
        ):
            self._invoice_counter = getattr(self, "_invoice_counter", 0) + 1
            vals["l10n_latam_document_number"] = f"001-001-{self._invoice_counter:07d}"
        if (
            move_type in ("out_invoice", "out_refund")
            and "l10n_py_authorization_id" not in kwargs
        ):
            vals["l10n_py_authorization_id"] = (
                self.authorization_nc.id
                if doc_type == self.doc_type_nc
                else self.authorization.id
            )
        vals.update(kwargs)
        return self.env["account.move"].create(vals)

    def _create_libro(self, tipo_registro, **kwargs):
        vals = {
            "company_id": self.company.id,
            "tipo_registro": tipo_registro,
            "obligacion": "955",
            "year": self.TEST_YEAR,
            "month": self.TEST_MONTH,
        }
        vals.update(kwargs)
        return self.env["l10n_py.libro"].create(vals)
