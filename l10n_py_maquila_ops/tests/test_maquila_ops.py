# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestMaquilaOps(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.py = cls.env.ref("base.py")
        cls.matriz = cls.env["res.partner"].create({"name": "Ops Matriz"})
        cls.program = cls.env["l10n_py.maquila.program"].create(
            {
                "name": "Ops Program",
                "code": "RES-BIM-OPS-001",
                "maquila_type": "pura",
                "matriz_partner_id": cls.matriz.id,
                "company_id": cls.company.id,
                "state": "active",
                "internal_sale_pct": 10.0,
            }
        )
        cls.product = cls.env["product.product"].create(
            {"name": "Ops Product", "is_storable": True, "list_price": 100.0}
        )

    # ---------- admission ----------
    def _admission(self, cif=40000, guarantee=None, cert="CN-1"):
        return self.env["l10n_py.maquila.admission"].create(
            {
                "name": f"DI-OPS-{cert}",
                "program_id": self.program.id,
                "guarantee_id": guarantee and guarantee.id,
                "cnime_certificate": cert,
                "amount_cif": cif,
                "line_ids": [(0, 0, {"product_id": self.product.id, "quantity": 100})],
            }
        )

    def test_admission_deadline(self):
        adm = self._admission()
        expected = adm.date_admission + relativedelta(months=12)
        self.assertEqual(adm.date_deadline, expected)

    def test_admission_qty_remaining_no_outflow(self):
        adm = self._admission()
        line = adm.line_ids
        # No stock has left the admission location yet.
        self.assertEqual(line.qty_consumed, 0.0)
        self.assertEqual(line.qty_remaining, line.quantity)

    def test_admission_requires_cnime(self):
        adm = self._admission(cert="")
        adm.cnime_certificate = False
        with self.assertRaises(UserError):
            adm.action_admit()

    def test_admission_extend_once(self):
        adm = self._admission()
        adm.action_admit()
        adm.action_extend()
        self.assertEqual(
            adm.date_extended, adm.date_deadline + relativedelta(months=12)
        )
        with self.assertRaises(UserError):
            adm.action_extend()

    def _typed_admission(self, good_type, **kw):
        vals = {
            "name": f"DI-OPS-{good_type}",
            "program_id": self.program.id,
            "cnime_certificate": "CN-T",
            "good_type": good_type,
            "date_admission": "2026-01-15",
            "line_ids": [(0, 0, {"product_id": self.product.id, "quantity": 1})],
        }
        vals.update(kw)
        return self.env["l10n_py.maquila.admission"].create(vals)

    def test_art14_raw_material_12_months_extendable(self):
        adm = self._typed_admission("raw_material_input")
        self.assertEqual(str(adm.date_deadline), "2027-01-15")
        adm.action_admit()
        adm.action_extend()
        self.assertEqual(str(adm.date_extended), "2028-01-15")

    def test_art14_container_12_months_from_arrival_no_extension(self):
        adm = self._typed_admission("container_box", date_arrival="2026-03-01")
        # counted from the arrival declaration, not from the import date
        self.assertEqual(str(adm.date_deadline), "2027-03-01")
        adm.action_admit()
        with self.assertRaises(UserError):
            adm.action_extend()

    def test_art14_container_requires_arrival_date(self):
        adm = self._typed_admission("container_box")
        self.assertFalse(adm.date_deadline)
        with self.assertRaises(UserError):
            adm.action_admit()

    def test_art14_capital_good_follows_program(self):
        self.program.write({"cnime_resolution_date": "2010-06-30"})  # +20 years
        adm = self._typed_admission("capital_good")
        self.assertEqual(str(adm.date_deadline), "2030-06-30")
        adm.action_admit()
        with self.assertRaises(UserError):
            adm.action_extend()

    # ---------- guarantee ----------
    def test_guarantee_amounts(self):
        guar = self.env["l10n_py.maquila.guarantee"].create(
            {
                "name": "Ops Guar",
                "program_id": self.program.id,
                "guarantee_type": "bank",
                "amount": 100000,
                "date_start": fields.Date.today(),
                "date_end": fields.Date.today() + relativedelta(years=1),
            }
        )
        self.assertEqual(guar.amount_available, 100000)
        adm = self._admission(cif=40000, guarantee=guar)
        adm.action_admit()
        self.assertEqual(guar.amount_available, 60000)

    def test_admission_guarantee_insufficient(self):
        guar = self.env["l10n_py.maquila.guarantee"].create(
            {
                "name": "Ops Guar2",
                "program_id": self.program.id,
                "guarantee_type": "bank",
                "amount": 30000,
                "date_start": fields.Date.today(),
                "date_end": fields.Date.today() + relativedelta(years=1),
            }
        )
        adm = self._admission(cif=90000, guarantee=guar, cert="CN-X")
        with self.assertRaises(UserError):
            adm.action_admit()

    def _guarantee(self, **kw):
        vals = {
            "name": "Ops Guar T",
            "program_id": self.program.id,
            "guarantee_type": "bank",
            "amount": 100000,
            "date_start": fields.Date.today() - relativedelta(months=1),
            "date_end": fields.Date.today() + relativedelta(years=1),
        }
        vals.update(kw)
        return self.env["l10n_py.maquila.guarantee"].create(vals)

    def test_guarantee_expiry_cron(self):
        old = self._guarantee(
            name="Old",
            date_start=fields.Date.today() - relativedelta(years=2),
            date_end=fields.Date.today() - relativedelta(days=1),
        )
        live = self._guarantee(name="Live")
        self.env["l10n_py.maquila.guarantee"]._cron_expire_guarantees()
        self.assertEqual(old.state, "expired")
        self.assertEqual(live.state, "active")

    def test_expired_guarantee_cannot_cover_admission(self):
        guar = self._guarantee(
            date_start=fields.Date.today() - relativedelta(years=2),
            date_end=fields.Date.today() - relativedelta(days=1),
        )
        adm = self._admission(cif=1000, guarantee=guar, cert="CN-EXP")
        with self.assertRaises(UserError):
            adm.action_admit()
        guar.state = "expired"
        with self.assertRaises(UserError):
            adm.action_admit()

    def test_guarantee_scope(self):
        op_guar = self._guarantee(name="Per operation")
        self._admission(cif=1000, guarantee=op_guar, cert="CN-S1")
        with self.assertRaises(ValidationError):
            self._admission(cif=1000, guarantee=op_guar, cert="CN-S2")
        global_guar = self._guarantee(name="Global", scope="global")
        self._admission(cif=1000, guarantee=global_guar, cert="CN-S3")
        self._admission(cif=1000, guarantee=global_guar, cert="CN-S4")
        self.assertEqual(len(global_guar.admission_ids), 2)

    def test_guarantee_not_yet_valid_rejected(self):
        guar = self._guarantee(
            name="Future", date_start=fields.Date.today() + relativedelta(days=5)
        )
        adm = self._admission(cif=1000, guarantee=guar, cert="CN-FUT")
        with self.assertRaises(UserError):
            adm.action_admit()

    def test_operation_guarantee_released_by_closed_admission(self):
        guar = self._guarantee(name="Reusable")
        first = self._admission(cif=1000, guarantee=guar, cert="CN-R1")
        first.state = "closed"
        self._admission(cif=1000, guarantee=guar, cert="CN-R2")
        with self.assertRaises(ValidationError):
            self._admission(cif=1000, guarantee=guar, cert="CN-R3")

    def test_cap_override_fields_in_sale_order_form(self):
        manager_group = self.env.ref("l10n_py_maquila_base.group_maquila_manager")
        self.env.user.write({"group_ids": [(4, manager_group.id)]})
        views = self.env["sale.order"].get_views([(False, "form")])
        arch = views["views"]["form"]["arch"]
        self.assertIn("l10n_py_maquila_cap_override_reason", arch)

    def test_guarantee_amount_used_converted(self):
        other = self.env.ref("base.EUR")
        other.active = True
        self.env["res.currency.rate"].create(
            {
                "currency_id": other.id,
                "company_id": self.company.id,
                "name": fields.Date.today() - relativedelta(days=30),
                "rate": 0.5,  # 1 company-currency unit = 0.5 EUR
            }
        )
        guar = self._guarantee(
            currency_id=self.company.currency_id.id, scope="global", amount=10**9
        )
        adm = self._admission(cif=1000, guarantee=guar, cert="CN-CUR")
        adm.currency_id = other
        adm.action_admit()
        expected = other._convert(
            1000, self.company.currency_id, self.company, adm.date_admission
        )
        self.assertAlmostEqual(guar.amount_used, expected)
        self.assertNotEqual(guar.amount_used, 1000)

    # ---------- export ----------
    def test_export_traceability(self):
        exp = self.env["l10n_py.maquila.export"].create(
            {"name": "EXP-OPS-1", "program_id": self.program.id}
        )
        with self.assertRaises(UserError):
            exp.action_confirm()
        adm = self._admission(cert="CN-EXP")
        exp.admission_ids = [(6, 0, [adm.id])]
        exp.action_confirm()
        self.assertEqual(exp.state, "confirmed")

    # ---------- TUM wizard ----------
    def _accounts(self):
        journal = self.env["account.journal"].search(
            [("type", "=", "general"), ("company_id", "=", self.company.id)], limit=1
        )
        if not journal:
            journal = self.env["account.journal"].create(
                {"name": "Misc", "code": "MISC", "type": "general"}
            )
        exp_acc = self.env["account.account"].search(
            [("account_type", "=", "expense")], limit=1
        ) or self.env["account.account"].create(
            {"name": "Exp", "code": "EXP1", "account_type": "expense"}
        )
        pay_acc = self.env["account.account"].search(
            [("account_type", "=", "liability_current")], limit=1
        ) or self.env["account.account"].create(
            {"name": "Pay", "code": "PAY1", "account_type": "liability_current"}
        )
        return journal, exp_acc, pay_acc

    def test_tum_wizard(self):
        _j, exp_acc, pay_acc = self._accounts()
        wiz = self.env["l10n_py.maquila.tum.wizard"].create(
            {
                "program_id": self.program.id,
                "period_start": "2026-01-01",
                "period_end": "2026-12-31",
                "van_amount": 30000,
                "export_invoice_amount": 50000,
                "tum_rate": 1.0,
                "debit_account_id": exp_acc.id,
                "credit_account_id": pay_acc.id,
            }
        )
        self.assertEqual(wiz.tum_base, 50000)
        self.assertEqual(wiz.tum_amount, 500)
        res = wiz.action_generate_move()
        move = self.env["account.move"].browse(res["res_id"])
        self.assertEqual(move.l10n_py_maquila_program_id, self.program)
        self.assertEqual(len(move.line_ids), 2)

    def test_tax_credit_wizard(self):
        _j, exp_acc, pay_acc = self._accounts()
        wiz = self.env["l10n_py.maquila.tax.credit.wizard"].create(
            {
                "program_id": self.program.id,
                "action_type": "compensate",
                "amount": 1000,
                "debit_account_id": exp_acc.id,
                "credit_account_id": pay_acc.id,
            }
        )
        res = wiz.action_execute()
        move = self.env["account.move"].browse(res["res_id"])
        self.assertEqual(move.l10n_py_maquila_program_id, self.program)

    # ---------- domestic sales cap (Ley 7547/2025 Art. 18) ----------
    def _prior_year_export(self, fob, program=None):
        year = fields.Date.today().year - 1
        self.env["l10n_py.maquila.export"].create(
            {
                "name": "EXP-PRIOR",
                "program_id": (program or self.program).id,
                "currency_id": self.company.currency_id.id,
                "date_export": f"{year}-06-01",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "fob_value": fob,
                        },
                    )
                ],
            }
        )

    def _domestic_sale(self, qty, program=None):
        customer = self.env["res.partner"].create(
            {"name": "PY Customer", "country_id": self.py.id}
        )
        return self.env["sale.order"].create(
            {
                "partner_id": customer.id,
                "l10n_py_maquila_program_id": (program or self.program).id,
                "order_line": [
                    (0, 0, {"product_id": self.product.id, "product_uom_qty": qty})
                ],
            }
        )

    def test_domestic_sale_within_cap(self):
        self._prior_year_export(100000)  # cap = 10% = 10000
        order = self._domestic_sale(50)  # 50 * 100 = 5000
        order.action_confirm()
        self.assertEqual(order.state, "sale")

    def test_domestic_sale_exceeds_cap(self):
        self._prior_year_export(100000)  # cap = 10000
        order = self._domestic_sale(200)  # 200 * 100 = 20000 > 10000
        with self.assertRaises(UserError):
            order.action_confirm()

    def test_domestic_sale_no_prior_export_blocked(self):
        # Pure maquila without exports in the last year: cap == 0 (Art. 18).
        order = self._domestic_sale(200)
        with self.assertRaises(UserError):
            order.action_confirm()
        self.assertNotEqual(order.state, "sale")

    def test_domestic_sale_cap_override_audited(self):
        manager = self.env["res.users"].create(
            {
                "name": "Maquila Manager",
                "login": "maquila_cap_manager",
                "email": "maquila.manager@example.com",
                "group_ids": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_user").id,
                            self.env.ref("sales_team.group_sale_manager").id,
                            # mrp (installed by the next modules) looks up BoM
                            # kits as the confirming user
                            self.env.ref("stock.group_stock_user").id,
                            self.env.ref(
                                "l10n_py_maquila_base.group_maquila_manager"
                            ).id,
                        ],
                    )
                ],
            }
        )
        order = self._domestic_sale(200).with_user(manager)
        order.l10n_py_maquila_cap_override = True
        # an override without reason is refused
        with self.assertRaises(UserError):
            order.action_confirm()
        order.l10n_py_maquila_cap_override_reason = "Authorized by Secretaria Ejecutiva"
        order.action_confirm()
        self.assertEqual(order.state, "sale")
        self.assertTrue(any("overridden" in (m.body or "") for m in order.message_ids))

    def test_domestic_sale_cap_override_denied_without_group(self):
        order = self._domestic_sale(200)
        order.sudo().write(
            {
                "l10n_py_maquila_cap_override": True,
                "l10n_py_maquila_cap_override_reason": "no group",
            }
        )
        user = self.env["res.users"].create(
            {
                "name": "Plain Salesman",
                "login": "maquila_plain_sales",
                "group_ids": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_user").id,
                            self.env.ref("sales_team.group_sale_manager").id,
                            self.env.ref("stock.group_stock_user").id,
                            self.env.ref("l10n_py_maquila_base.group_maquila_user").id,
                        ],
                    )
                ],
            }
        )
        with self.assertRaisesRegex(UserError, "Only Maquila managers"):
            order.with_user(user).action_confirm()

    def _plain_salesman(self):
        return self.env["res.users"].create(
            {
                "name": "Plain Salesman",
                "login": "maquila_plain_sales",
                "group_ids": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_user").id,
                            self.env.ref("sales_team.group_sale_manager").id,
                            self.env.ref("stock.group_stock_user").id,
                        ],
                    )
                ],
            }
        )

    def test_domestic_sale_within_cap_without_maquila_group(self):
        self._prior_year_export(100000)  # cap = 10000
        order = self._domestic_sale(50)  # 5000
        order.with_user(self._plain_salesman()).action_confirm()
        self.assertEqual(order.state, "sale")

    def test_domestic_sale_exceeds_cap_without_maquila_group(self):
        self._prior_year_export(100000)  # cap = 10000
        order = self._domestic_sale(200)  # 20000
        with self.assertRaisesRegex(UserError, "would exceed"):
            order.with_user(self._plain_salesman()).action_confirm()

    def test_domestic_cap_skipped_for_non_pura(self):
        # A separate program so it does not affect the shared "pura" one.
        prog = self.env["l10n_py.maquila.program"].create(
            {
                "name": "Ops Ociosidad",
                "code": "RES-BIM-OPS-OCI",
                "maquila_type": "ociosidad",
                "matriz_partner_id": self.matriz.id,
                "company_id": self.company.id,
                "state": "active",
            }
        )
        self._prior_year_export(100000, program=prog)  # cap would be 10000 if pura
        order = self._domestic_sale(500, program=prog)  # 50000, over — but not pura
        order.action_confirm()
        self.assertEqual(order.state, "sale")

    # ---------- fiscal position on export orders ----------
    def _py_chart_company(self, name):
        """A company with the real l10n_py chart loaded (fiscal positions,
        including the auto_apply "Ventas - Exportación" one, and taxes)."""
        company = self.env["res.company"].create({"name": name})
        self.env["account.chart.template"].try_loading(
            "py", company=company, install_demo=False
        )
        return company

    def _foreign_partner(self, name="Foreign Matriz"):
        return self.env["res.partner"].create(
            {"name": name, "country_id": self.env.ref("base.br").id}
        )

    def _maquila_export_order(self, company, program):
        foreign = self._foreign_partner()
        order = self.env["sale.order"].create(
            {"partner_id": foreign.id, "company_id": company.id}
        )
        # Simulate what Odoo's own onchange machinery does when the
        # quotation partner is set: auto-detect the fiscal position first.
        order.fiscal_position_id = (
            self.env["account.fiscal.position"]
            .with_company(company)
            ._get_fiscal_position(foreign)
        )
        order.l10n_py_maquila_program_id = program
        order._onchange_maquila_program()
        return order

    def test_maquila_export_keeps_auto_detected_exoneration(self):
        """A maquila export order for a foreign partner must not lose the
        chart's auto-detected "Ventas - Exportación" fiscal position (which
        maps VAT to exonerado) in favor of the maquila position, which has
        no tax mapping of its own."""
        if not self.env["ir.module.module"].search_count(
            [("name", "=", "l10n_py_account"), ("state", "=", "installed")]
        ):
            self.skipTest(
                "needs l10n_py_account (auto-detected export fiscal position)"
            )
        company = self._py_chart_company("PY Maquila Export Co")
        program = self.env["l10n_py.maquila.program"].create(
            {
                "name": "Export FP Program",
                "code": "RES-BIM-OPS-FP1",
                "maquila_type": "pura",
                "matriz_partner_id": self.matriz.id,
                "company_id": company.id,
                "state": "active",
            }
        )
        vat10 = (
            self.env["account.tax"]
            .with_company(company)
            .search(
                [
                    ("company_id", "=", company.id),
                    ("type_tax_use", "=", "sale"),
                    ("amount", "=", 10),
                ],
                limit=1,
            )
        )
        self.assertTrue(vat10, "the l10n_py chart must provide a 10% sale tax")

        order = self._maquila_export_order(company, program)

        self.assertEqual(order.fiscal_position_id.name, "Ventas - Exportación")
        mapped = order.fiscal_position_id.map_tax(vat10)
        self.assertEqual(
            mapped.l10n_py_iva_affectation,
            "2",
            "a maquila export must end with exonerated VAT, not 10%",
        )
