# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import binascii
import math

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.mimetypes import guess_mimetype


class QcInspection(models.Model):
    _inherit = "qc.inspection"

    barcode_scanner_confirmed = fields.Boolean(
        string="Confirmed from the scanner",
        copy=False,
        readonly=True,
        help="Confirmed from the Barcode app: the operator may put it back to "
        "draft from there while no supervisor has decided it and the reception "
        "is still open.",
    )

    def _barcode_scanner_read_lines(self):
        """Serialise an inspection's questions for the scanner UI."""
        self.ensure_one()
        lines = []
        for line in self.inspection_lines:
            lines.append(
                {
                    "id": line.id,
                    "name": line.name,
                    "question_type": line.question_type,
                    "notes": line.notes or "",
                    "min_value": line.min_value,
                    "max_value": line.max_value,
                    "uom_name": line.test_uom_id.display_name or "",
                    "qualitative_value_id": line.qualitative_value.id,
                    "qualitative_value_name": line.qualitative_value.name or "",
                    "quantitative_value": line.quantitative_value,
                    "success": line.success,
                    "possible_values": [
                        {"id": value.id, "name": value.name, "ok": value.ok}
                        for value in line.possible_ql_values
                    ],
                }
            )
        return lines

    def _barcode_scanner_read(self):
        self.ensure_one()
        return {
            "inspection_id": self.id,
            "inspection_name": self.name,
            "product_name": self.product_id.display_name or "",
            "lot_name": self.lot_id.name or "",
            "test_name": self.test.display_name or "",
            "state": self.state,
            "success": self.success,
            "can_reset": self._barcode_scanner_can_reset(),
            "photo_count": self._barcode_scanner_photo_count(),
            "lines": self._barcode_scanner_read_lines(),
        }

    def _barcode_scanner_can_reset(self):
        """Whether the scanner may put the inspection back to draft: only one
        it confirmed itself, that no supervisor has decided yet (a ``failed``
        inspection is a supervisor's rejection), on a reception still open.
        The back office does not reopen confirmed inspections; the scanner only
        lets the operator correct their own confirmation."""
        self.ensure_one()
        return (
            self.barcode_scanner_confirmed
            and self.state in ("success", "waiting")
            and self.picking_id.state not in ("done", "cancel")
        )

    def _barcode_scanner_photo_count(self):
        self.ensure_one()
        return self.env["ir.attachment"].search_count(
            [
                ("res_model", "=", self._name),
                ("res_id", "=", self.id),
                ("mimetype", "=like", "image/%"),
            ]
        )

    @api.model
    def _barcode_scanner_inspection(self, inspection_id):
        inspection = self.browse(inspection_id).exists()
        if not inspection:
            raise UserError(self.env._("The inspection no longer exists."))
        return inspection

    def _barcode_scanner_answer(self, line, answer):
        """Write the operator's answer to one question.

        Every question needs its answer: a measure left blank would otherwise
        be judged as 0, and a choice must be one the question offers.
        """
        if line.question_type == "qualitative":
            value = self.env["qc.test.question.value"].browse(
                (answer or {}).get("qualitative_value_id") or []
            )
            if not value or value not in line.possible_ql_values:
                raise UserError(
                    self.env._(
                        "Choose one of the answers offered for %(question)s.",
                        question=line.name,
                    )
                )
            line.qualitative_value = value
            return
        try:
            measure = float((answer or {}).get("quantitative_value"))
        except (TypeError, ValueError):
            measure = math.nan
        if not math.isfinite(measure):
            raise UserError(
                self.env._(
                    "Enter the value measured for %(question)s.", question=line.name
                )
            )
        line.uom_id = line.test_uom_id
        line.quantitative_value = measure

    @api.model
    def action_barcode_scanner_submit(self, inspection_id, answers):
        """Record the operator's answers and confirm the inspection.

        ``answers`` is a list of ``{line_id, qualitative_value_id}`` for
        qualitative questions and ``{line_id, quantitative_value}`` for
        quantitative ones, one per question. Returns the resulting inspection.
        """
        inspection = self._barcode_scanner_inspection(inspection_id)
        if inspection.state != "ready":
            raise UserError(
                self.env._("This inspection cannot be edited in its current state.")
            )

        answers_by_line = {answer.get("line_id"): answer for answer in answers or []}
        for line in inspection.inspection_lines:
            inspection._barcode_scanner_answer(line, answers_by_line.get(line.id))
        inspection.action_confirm()
        inspection.barcode_scanner_confirmed = True
        return inspection._barcode_scanner_read()

    @api.model
    def action_barcode_scanner_reset(self, inspection_id):
        """Put back to draft an inspection the operator confirmed from the
        scanner, to correct it (see ``_barcode_scanner_can_reset``).

        Its answers are kept, and the scanner shows them filled in: the
        operator changes what was wrong and confirms again. Draft, then mark
        todo in one step: a draft inspection is not runnable from the scanner,
        so it is left ``ready``.
        """
        inspection = self._barcode_scanner_inspection(inspection_id)
        if not inspection._barcode_scanner_can_reset():
            raise UserError(
                self.env._(
                    "Only an inspection confirmed from the scanner, not yet "
                    "decided by a supervisor, on a reception still open, can be "
                    "put back to draft here."
                )
            )
        inspection.action_draft()
        inspection.action_todo()
        inspection.barcode_scanner_confirmed = False
        return inspection._barcode_scanner_read()

    @api.model
    def action_barcode_scanner_attach_photo(self, inspection_id, filename, datas):
        """Attach a photo as evidence to an inspection.

        ``datas`` is the base64-encoded image content coming from the scanner.
        The attachment is linked to the inspection so it shows in its chatter.
        Only an image is taken: this is evidence for a check, not any file.
        """
        inspection = self._barcode_scanner_inspection(inspection_id)
        try:
            content = base64.b64decode(datas or "", validate=True)
        except (binascii.Error, ValueError) as err:
            raise UserError(self.env._("The photo could not be read.")) from err
        if not guess_mimetype(content).startswith("image/"):
            raise UserError(self.env._("Only a photo can be attached as evidence."))
        try:
            self.env["ir.attachment"].create(
                {
                    "name": filename or self.env._("Quality evidence"),
                    "datas": datas,
                    "res_model": inspection._name,
                    "res_id": inspection.id,
                }
            )
        except OSError as err:
            # A truncated or corrupt image trips Odoo's image post-processing.
            raise UserError(self.env._("The photo could not be saved.")) from err
        return {
            "inspection_id": inspection.id,
            "photo_count": inspection._barcode_scanner_photo_count(),
        }
