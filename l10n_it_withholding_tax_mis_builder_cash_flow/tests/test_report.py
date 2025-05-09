# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests import tagged

from odoo.addons.l10n_it_withholding_tax_mis_builder.tests.common import (
    WithholdingTaxReportCommon,
)


@tagged("post_install", "-at_install")
class TestWithholdingTaxReport(WithholdingTaxReportCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)

        cls.cash_flow_model = cls.env.ref("mis_builder_cash_flow.model_mis_cash_flow")

        cls.report_template.move_lines_source = cls.cash_flow_model

    def test_report_to_pay_amount(self):
        """Check that the MIS Report with cash flow shows the amount to be paid."""
        # Arrange
        total_amount = 115
        to_pay_amount = 95
        invoice = self.invoice
        # pre-condition
        self.assertEqual(
            self.report_instance.report_id.move_lines_source,
            self.cash_flow_model,
        )
        self.assertRecordValues(
            invoice,
            [
                {
                    "amount_total": total_amount,
                    "amount_net_pay": to_pay_amount,
                }
            ],
        )

        # Act
        matrix = self.report_instance._compute_matrix()

        # Assert
        for row in matrix.iter_rows():
            if row.kpi.name == "pay_bal":
                cell = next(row.iter_cells())
                self.assertEqual(-to_pay_amount, cell.val)
                break
        else:
            self.fail("Payable KPI not found")
