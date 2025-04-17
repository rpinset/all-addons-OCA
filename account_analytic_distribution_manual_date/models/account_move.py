# Copyright 2024 (APSL - Nagarro) Bernat Obrador
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def write(self, vals):
        for record in self:
            date = self._get_invoice_date(vals, record)
            invoice_line_ids = vals.get("invoice_line_ids", [])

            if invoice_line_ids:
                self._validate_manual_distributions(
                    invoice_line_ids, date, from_vals=True
                )
            elif "invoice_date" in vals:
                self._validate_manual_distributions(record.invoice_line_ids, date)

        return super().write(vals)

    def _get_invoice_date(self, vals, record):
        date_string = (
            vals.get("invoice_date")
            or record.invoice_date
            or vals.get("date")
            or record.date
        )
        return (
            fields.Date.from_string(date_string)
            if date_string
            else fields.Date.context_today(self)
        )

    def _validate_manual_distributions(self, lines, date, from_vals=False):
        for line in lines:
            manual_distribution = None
            if from_vals:
                if len(line) > 2 and "manual_distribution_id" in line[2]:
                    manual_distribution = self.env[
                        "account.analytic.distribution.manual"
                    ].browse(line[2]["manual_distribution_id"])
            else:
                manual_distribution = line.manual_distribution_id
            if manual_distribution:
                self._check_manual_distribution_date(manual_distribution, date)

    def _check_manual_distribution_date(self, manual_distribution, date):
        start_date = manual_distribution.start_date
        end_date = manual_distribution.end_date

        if start_date and end_date and not (start_date <= date <= end_date):
            raise UserError(
                _(
                    "The invoice date %(invoice_date)s is outside the "
                    "manual distribution period %(start_date)s - "
                    "%(end_date)s."
                )
                % {
                    "invoice_date": date,
                    "start_date": start_date,
                    "end_date": end_date,
                }
            )

        elif start_date and not end_date and date < start_date:
            raise UserError(
                _(
                    "The invoice date %(invoice_date)s is before the "
                    "manual distribution start date %(start_date)s."
                )
                % {
                    "invoice_date": date,
                    "start_date": start_date,
                }
            )

        elif not start_date and end_date and date > end_date:
            raise UserError(
                _(
                    "The invoice date %(invoice_date)s is after the "
                    "manual distribution end date %(end_date)s."
                )
                % {
                    "invoice_date": date,
                    "end_date": end_date,
                }
            )
