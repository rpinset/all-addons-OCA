# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests import tagged

from odoo.addons.l10n_it_withholding_tax_mis_builder.tests.common import (
    WithholdingTaxReportCommon,
)


@tagged("post_install", "-at_install")
class TestWithholdingTaxReport(WithholdingTaxReportCommon):
    def test_report_to_pay_amount(self):
        """Check that the MIS Report shows the amount to be paid."""
        # Arrange
        total_amount = 115
        to_pay_amount = 95
        invoice = self.invoice
        # pre-condition
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
