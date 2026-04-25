# Copyright 2024 Dixmit
# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    # add_payment_lot_id is a technical field used by the bank statement reconcile
    # interface: when the user clicks on a payment lot, the onchange of this field is
    # called.
    add_payment_lot_id = fields.Many2one(
        "account.payment.lot",
        check_company=True,
        prefetch=False,
    )

    def clean_reconcile(self):
        """
        Remove the counterparts when cleaning
        """
        res = super().clean_reconcile()
        self.reconcile_data_info["payment_lot_counterparts"] = []
        return res

    @api.onchange("add_payment_lot_id")
    def _onchange_add_payment_lot_id(self):
        """
        We need to check if the payment order is in already on the counterpart.
        In this case we need to add all the liquidity lines. Otherwise, we remove them
        """
        if self.add_payment_lot_id:
            self._add_payment_lot(self.add_payment_lot_id)
            self.add_payment_lot_id = False

    def _add_payment_lot(self, lot):
        new_data = []
        if lot.id not in self.reconcile_data_info.get("payment_lot_counterparts", []):
            # The user has selected a lot that has not already been selected
            counterpart_lines = []
            for line in self.reconcile_data_info["data"]:
                counterpart_lines += line.get("counterpart_line_ids", [])
                new_data.append(line)
            candidate_move_lines = lot._get_move_lines_to_reconcile()

            for line in candidate_move_lines.filtered(
                lambda r: r.id not in counterpart_lines
            ):
                reconcile_auxiliary_id, lines = self._get_reconcile_line(
                    line, "other", True, 0.0
                )
                new_data += lines

            data_info = self._recompute_suspense_line(
                new_data,
                self.reconcile_data_info["reconcile_auxiliary_id"],
                self.manual_reference,
            )
            data_info["payment_lot_counterparts"].append(lot.id)
        else:
            # The user selected a lot that has already been selected
            # for that statement line
            move_lines = lot._get_move_lines_to_reconcile()
            new_data = []
            for line in self.reconcile_data_info["data"]:
                if set(line.get("counterpart_line_ids", [])).intersection(
                    set(move_lines.ids)
                ):
                    continue
                new_data.append(line)
            data_info = self._recompute_suspense_line(
                new_data,
                self.reconcile_data_info["reconcile_auxiliary_id"],
                self.manual_reference,
            )
            lot_counterparts = set(data_info["payment_lot_counterparts"])
            lot_counterparts.remove(lot.id)
            data_info["payment_lot_counterparts"] = list(lot_counterparts)
        self.can_reconcile = data_info.get("can_reconcile", False)
        self.reconcile_data_info = data_info

    def _recompute_suspense_line(self, data, reconcile_auxiliary_id, manual_reference):
        """
        We want to keep the counterpart when we recompute
        """
        result = super()._recompute_suspense_line(
            data, reconcile_auxiliary_id, manual_reference
        )
        payment_lot_counterparts = (
            self.reconcile_data_info
            and self.reconcile_data_info.get("payment_lot_counterparts", [])
        ) or []
        result["payment_lot_counterparts"] = payment_lot_counterparts
        return result

    def add_multiple_lines(self, domain):
        """Method called by the button 'Add all'"""
        if ["state", "=", "uploaded"] in domain:
            # called from the "Payment lots" tab
            lots = self.env["account.payment.lot"].search(domain)
            for lot in lots:
                self._add_payment_lot(lot)
        else:
            # called from the "Reconcile" tab
            return super().add_multiple_lines(domain)
