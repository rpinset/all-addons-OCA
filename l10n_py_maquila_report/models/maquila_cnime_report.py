# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class MaquilaCnimeReport(models.Model):
    _name = "l10n_py.maquila.cnime.report"
    _description = "CNIME Periodic Report"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "period_start desc"

    name = fields.Char(compute="_compute_name", store=True)
    program_id = fields.Many2one(
        "l10n_py.maquila.program",
        required=True,
        tracking=True,
    )
    period_start = fields.Date(required=True, tracking=True)
    period_end = fields.Date(required=True, tracking=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("generated", "Generated"),
            ("validated", "Validated"),
            ("submitted", "Submitted"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )
    # Snapshot fields, filled by action_generate() and frozen afterwards
    # (a periodic report must not silently recompute after submission).
    import_data = fields.Text(readonly=True)
    export_data = fields.Text(readonly=True)
    production_data = fields.Text(readonly=True)
    waste_data = fields.Text(readonly=True)
    stock_balance = fields.Text(readonly=True)
    employment_count = fields.Integer()
    van_total = fields.Monetary(string="VAN Total", readonly=True)
    currency_id = fields.Many2one(
        related="company_id.currency_id",
        string="Currency",
        store=True,
        help="Company currency: the VAN is built from analytic amounts, which "
        "are always in the company currency.",
    )
    submission_date = fields.Datetime(tracking=True)
    submission_protocol = fields.Char(tracking=True)
    company_id = fields.Many2one(
        related="program_id.company_id",
        store=True,
    )

    @api.depends("program_id.code", "period_start", "period_end")
    def _compute_name(self):
        for report in self:
            report.name = self.env._(
                "CNIME %(program)s %(start)s - %(end)s",
                program=report.program_id.code or "",
                start=report.period_start or "",
                end=report.period_end or "",
            )

    def _generate_report_data(self):
        """Compile the report snapshot. Called explicitly by action_generate,
        never as a compute, so a submitted report is never silently rewritten."""
        for report in self:
            if not (report.program_id and report.period_start and report.period_end):
                raise UserError(
                    self.env._("Set the program and the period before generating.")
                )
            program = report.program_id

            # Import data - admissions in period
            admissions = self.env["l10n_py.maquila.admission"].search(
                [
                    ("program_id", "=", program.id),
                    ("date_admission", ">=", report.period_start),
                    ("date_admission", "<=", report.period_end),
                ]
            )
            import_lines = []
            for adm in admissions:
                for line in adm.line_ids:
                    import_lines.append(
                        {
                            "dispatch": adm.name,
                            "product": line.product_id.name,
                            "quantity": line.quantity,
                            "fob_value": line.fob_value,
                            "currency": line.currency_id.name,
                        }
                    )
            report.import_data = (
                json.dumps(import_lines, indent=2) if import_lines else False
            )

            # Export data - exports in period
            exports = self.env["l10n_py.maquila.export"].search(
                [
                    ("program_id", "=", program.id),
                    ("date_export", ">=", report.period_start),
                    ("date_export", "<=", report.period_end),
                ]
            )
            export_lines = []
            for exp in exports:
                for line in exp.line_ids:
                    export_lines.append(
                        {
                            "dispatch": exp.name,
                            "product": line.product_id.name,
                            "quantity": line.quantity,
                            "fob_value": line.fob_value,
                            "currency": line.currency_id.name,
                        }
                    )
            report.export_data = (
                json.dumps(export_lines, indent=2) if export_lines else False
            )

            # Production data
            productions = self.env["mrp.production"].search(
                [
                    ("l10n_py_maquila_program_id", "=", program.id),
                    ("date_start", ">=", report.period_start),
                    ("date_start", "<=", report.period_end),
                    ("state", "=", "done"),
                ]
            )
            prod_lines = []
            for prod in productions:
                prod_lines.append(
                    {
                        "reference": prod.name,
                        "product": prod.product_id.name,
                        "quantity": prod.product_qty,
                    }
                )
            report.production_data = (
                json.dumps(prod_lines, indent=2) if prod_lines else False
            )

            # Waste data
            wastes = self.env["l10n_py.maquila.waste"].search(
                [
                    ("program_id", "=", program.id),
                    ("date", ">=", report.period_start),
                    ("date", "<=", report.period_end),
                ]
            )
            waste_lines = []
            for w in wastes:
                waste_lines.append(
                    {
                        "product": w.product_id.name,
                        "quantity": w.quantity,
                        "type": w.waste_type,
                        "destination": w.destination,
                    }
                )
            report.waste_data = (
                json.dumps(waste_lines, indent=2) if waste_lines else False
            )

            # Stock balance at period_end (historical), from done stock moves
            # in/out of the maquila location tree up to the cut-off date.
            maquila_loc = self.env.ref(
                "l10n_py_maquila_ops.stock_location_maquila",
                raise_if_not_found=False,
            )
            balance_lines = []
            if maquila_loc:
                dt_to = fields.Datetime.to_datetime(report.period_end) + relativedelta(
                    days=1
                )
                move_line = self.env["stock.move.line"]
                base = [
                    ("state", "=", "done"),
                    ("date", "<", dt_to),
                    ("company_id", "=", program.company_id.id),
                ]
                incoming = move_line._read_group(
                    base + [("location_dest_id", "child_of", maquila_loc.id)],
                    ["product_id"],
                    ["quantity:sum"],
                )
                outgoing = move_line._read_group(
                    base + [("location_id", "child_of", maquila_loc.id)],
                    ["product_id"],
                    ["quantity:sum"],
                )
                balance = {}
                for product, qty in incoming:
                    balance[product] = balance.get(product, 0.0) + qty
                for product, qty in outgoing:
                    balance[product] = balance.get(product, 0.0) - qty
                for product, qty in balance.items():
                    if qty:
                        balance_lines.append({"product": product.name, "quantity": qty})
            report.stock_balance = (
                json.dumps(balance_lines, indent=2) if balance_lines else False
            )

            # VAN total via the shared program method (same figure as the wizard)
            try:
                report.van_total = program._maquila_van_for_period(
                    report.period_start, report.period_end
                )["van_amount"]
            except UserError:
                # No analytic account or no completed production in the period.
                report.van_total = 0.0

    def action_generate(self):
        """Compile the snapshot and move to the generated state."""
        for report in self:
            if report.state == "submitted":
                raise UserError(self.env._("A submitted report cannot be regenerated."))
        self._generate_report_data()
        self.write({"state": "generated"})

    def action_validate(self):
        self.write({"state": "validated"})

    def action_submit(self):
        self.write(
            {
                "state": "submitted",
                "submission_date": fields.Datetime.now(),
            }
        )

    def action_draft(self):
        for report in self:
            if report.state == "submitted":
                raise UserError(
                    self.env._("A submitted report cannot be reset to draft.")
                )
        self.write({"state": "draft"})

    def action_generate_simex_payload(self):
        """Generate a draft payload (stub for a future SIMEX integration).

        The layout is internal: it is not validated against the official SIMEX
        format, so it must not be filed as is."""
        self.ensure_one()
        # SIMEX integration stub - offline payload generation
        payload = {
            "programa": self.program_id.code,
            "periodo_inicio": str(self.period_start),
            "periodo_fin": str(self.period_end),
            "importaciones": json.loads(self.import_data or "[]"),
            "exportaciones": json.loads(self.export_data or "[]"),
            "produccion": json.loads(self.production_data or "[]"),
            "residuos": json.loads(self.waste_data or "[]"),
            "van_total": self.van_total,
            "empleo": self.employment_count,
        }
        # Log payload for debugging
        self.message_post(
            body=self.env._(
                "Draft SIMEX payload (internal layout, not validated against "
                "the official SIMEX format):\n%s",
                json.dumps(payload, indent=2, default=str),
            ),
        )
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": self.env._("SIMEX Payload Generated"),
                "message": self.env._(
                    "SIMEX payload generated successfully (offline mode)."
                ),
                "sticky": False,
                "type": "success",
            },
        }
