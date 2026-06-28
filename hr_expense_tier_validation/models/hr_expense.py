# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.exceptions import ValidationError

BASE_EXCEPTION_FIELDS = [
    "message_follower_ids",
    "access_token",
    "message_main_attachment_id",
    "accounting_date",
]


class HrExpense(models.Model):
    _inherit = "hr.expense"

    def _get_exception_fields(self, extra_domain=None):
        company = self.company_id or self.sheet_id.company_id or self.env.company
        return (
            self.env["tier.validation.exception"]
            .sudo()
            .search(
                [
                    ("model_name", "=", "hr.expense"),
                    ("company_id", "in", [False] + company.ids),
                    "|",
                    ("group_ids", "in", self.env.user.groups_id.ids),
                    ("group_ids", "=", False),
                    *(extra_domain or []),
                ]
            )
            .mapped("field_ids.name")
        )

    def _get_validation_exceptions(self, extra_domain=None):
        exception_fields = self._get_exception_fields(extra_domain=extra_domain)
        return list(set(exception_fields + BASE_EXCEPTION_FIELDS))

    def _get_under_validation_exceptions(self):
        return self._get_validation_exceptions(
            extra_domain=[("allowed_to_write_under_validation", "=", True)]
        )

    def _get_after_validation_exceptions(self):
        return self._get_validation_exceptions(
            extra_domain=[("allowed_to_write_after_validation", "=", True)]
        )

    def _get_fields_to_write_validation(self, vals, records_exception_function):
        exceptions = records_exception_function()
        not_allowed_fields = [val for val in vals if val not in exceptions]

        not_allowed_field_names = []
        allowed_field_names = []
        for fld_name, fld_data in self.fields_get(
            not_allowed_fields + exceptions
        ).items():
            if fld_name in not_allowed_fields:
                not_allowed_field_names.append(fld_data["string"])
            else:
                allowed_field_names.append(fld_data["string"])
        return allowed_field_names, not_allowed_field_names

    def _get_sheet_validation_write_check(self):
        self.ensure_one()
        sheet = self.sheet_id
        if sheet.state == "submit":
            return "under", self._get_under_validation_exceptions
        if sheet.state in ("approve", "post", "done"):
            return "after", self._get_after_validation_exceptions
        return False, False

    def write(self, vals):
        for rec in self:
            sheet = rec.sheet_id
            if (
                sheet.state in ("submit", "approve", "post", "done")
                and sheet.review_ids
                and not sheet.rejected
                and not rec.env.context.get("skip_validation_check")
            ):
                validation_step, exception_function = (
                    rec._get_sheet_validation_write_check()
                )
                if not exception_function:
                    continue
                allowed_fields, not_allowed_fields = (
                    rec._get_fields_to_write_validation(vals, exception_function)
                )
                if not_allowed_fields:
                    raise ValidationError(
                        self.env._(
                            "You are not allowed to write those fields "
                            "%(validation_step)s validation.\n"
                            "- %(not_allowed_fields_str)s\n\n"
                            "Only those fields can be modified:\n"
                            "- %(allowed_fields_str)s",
                            validation_step=validation_step,
                            not_allowed_fields_str="\n- ".join(not_allowed_fields),
                            allowed_fields_str="\n- ".join(allowed_fields),
                        )
                    )
        return super().write(vals)
