# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import tagged

from ..services.request_builder import SifendeRequestBuilder
from .common import SifendeCommon


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestPygRounding(SifendeCommon):
    def term(self, days_and_percents):
        return self.env["account.payment.term"].create(
            {
                "name": "Plan de cuotas",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "value": "percent",
                            "value_amount": percent,
                            "delay_type": "days_after",
                            "nb_days": days,
                        },
                    )
                    for days, percent in days_and_percents
                ],
            }
        )

    def cash_rounding(self, strategy):
        return self.env["account.cash.rounding"].create(
            {
                "name": f"Redondeo a 50 {strategy}",
                "rounding": 50,
                "strategy": strategy,
                "rounding_method": "HALF-UP",
                "profit_account_id": self.account_income.id,
                "loss_account_id": self.account_income.id,
            }
        )

    def test_el_pago_de_contado_cubre_el_total_redondeado_a_50(self):
        move = self.make_move("fe", lines=[self.line(price=55125.0, tax=self.tax_5)])
        self.assertEqual(move.amount_total, 55125)
        payload = self.sent_payload(move)
        self.assertEqual([p["montoPago"] for p in payload["pagos"]], [55100])

    def test_un_total_multiplo_de_50_no_cambia(self):
        move = self.make_move("fe", lines=[self.line(price=362400.0)])
        payload = self.sent_payload(move)
        self.assertEqual([p["montoPago"] for p in payload["pagos"]], [362400])

    def test_el_redondeo_va_siempre_hacia_abajo(self):
        move = self.make_move("fe", lines=[self.line(price=362449.0)])
        payload = self.sent_payload(move)
        self.assertEqual(payload["pagos"][0]["montoPago"], 362400)

    def test_las_cuotas_30_70_cubren_el_total_redondeado_a_50(self):
        move = self.make_move(
            "fe",
            lines=[self.line(price=55125.0, tax=self.tax_5)],
            invoice_payment_term_id=self.term([(30, 30), (60, 70)]).id,
        )
        payload = self.sent_payload(move)
        amounts = [c["monto"] for c in payload["credito"]["detalleCuotas"]]
        self.assertEqual(amounts, [16530, 38570])
        self.assertEqual(sum(amounts), 55100)

    def test_las_cuotas_de_un_total_multiplo_de_50_siguen_iguales(self):
        move = self.make_move(
            "fe",
            lines=[self.line(price=362400.0)],
            invoice_payment_term_id=self.term([(30, 30), (60, 70)]).id,
        )
        payload = self.sent_payload(move)
        amounts = [c["monto"] for c in payload["credito"]["detalleCuotas"]]
        self.assertEqual(amounts, [108720, 253680])

    def test_el_resto_del_reparto_va_a_la_ultima_cuota(self):
        move = self.make_move(
            "fe",
            lines=[self.line(price=100099.0)],
            invoice_payment_term_id=self.term(
                [(30, 33.33), (60, 33.33), (90, 33.34)]
            ).id,
        )
        payload = self.sent_payload(move)
        amounts = [c["monto"] for c in payload["credito"]["detalleCuotas"]]
        self.assertEqual(sum(amounts), 100050)
        self.assertEqual(amounts[:2], [33347, 33347])
        self.assertEqual(amounts[2], 100050 - 33347 * 2)

    def test_varios_pagos_se_reparten_en_proporcion(self):
        builder = SifendeRequestBuilder(self.env, lambda _category, _code: "X")
        result = builder._distribute(
            [30000, 25125],
            builder._fiscal_total({"totalOperacion": 55125}, "PYG", 0),
            0,
        )
        self.assertEqual(result, [29986, 25114])
        self.assertEqual(sum(result), 55100)

    def test_otras_monedas_no_se_redondean_a_50(self):
        total = SifendeRequestBuilder._fiscal_total({"totalOperacion": 30.75}, "USD", 2)
        self.assertEqual(str(total), "30.75")

    def test_la_linea_de_redondeo_de_efectivo_no_va_como_item(self):
        move = self.make_move(
            "fe",
            lines=[self.line(price=55125.0, tax=self.tax_5)],
            invoice_cash_rounding_id=self.cash_rounding("add_invoice_line").id,
        )
        self.assertEqual(move.amount_total, 55150)
        payload = self.sent_payload(move)
        self.assertEqual(len(payload["items"]), 1)
        self.assertEqual([p["montoPago"] for p in payload["pagos"]], [55100])

    def test_el_redondeo_de_efectivo_en_el_impuesto_mayor_tambien_cuadra(self):
        move = self.make_move(
            "fe",
            lines=[self.line(price=55125.0, tax=self.tax_5)],
            invoice_cash_rounding_id=self.cash_rounding("biggest_tax").id,
        )
        payload = self.sent_payload(move)
        self.assertEqual(len(payload["items"]), 1)
        self.assertEqual([p["montoPago"] for p in payload["pagos"]], [55100])

    def test_las_cuotas_con_redondeo_de_efectivo_cubren_el_total_de_sifende(self):
        move = self.make_move(
            "fe",
            lines=[self.line(price=55125.0, tax=self.tax_5)],
            invoice_cash_rounding_id=self.cash_rounding("add_invoice_line").id,
            invoice_payment_term_id=self.term([(30, 30), (60, 70)]).id,
        )
        payload = self.sent_payload(move)
        amounts = [c["monto"] for c in payload["credito"]["detalleCuotas"]]
        self.assertEqual(sum(amounts), 55100)
        self.assertEqual(len(amounts), 2)
