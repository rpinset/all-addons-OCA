# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class MaquilaAdmission(models.Model):
    _name = "l10n_py.maquila.admission"
    _description = "Maquila Temporary Admission"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_admission desc"

    name = fields.Char(
        string="Dispatch Number",
        required=True,
        tracking=True,
        help="Dispatch number (e.g. DI-2026-00123)",
    )
    program_id = fields.Many2one(
        "l10n_py.maquila.program",
        required=True,
        tracking=True,
        domain="[('state', '=', 'active')]",
    )
    cnime_certificate = fields.Char(
        string="CNIME Certificate",
        tracking=True,
    )
    good_type = fields.Selection(
        [
            ("raw_material_input", "Raw Materials and Inputs"),
            ("container_box", "Containers and Trailer Boxes"),
            ("capital_good", "Machinery, Tools and Other Goods"),
        ],
        required=True,
        default="raw_material_input",
        tracking=True,
        help="Ley 7547/2025 Art. 14 stay limits per type of good:\n"
        "- Raw materials and inputs: 12 months from the import date, "
        "extendable once for up to the same period (biministerial "
        "resolution).\n"
        "- Containers and trailer boxes: 12 months maximum from the "
        "arrival declaration; no extension.\n"
        "- Other goods (machinery, tools, equipment): while the Maquila "
        "program remains in force.",
    )
    date_admission = fields.Date(
        string="Import Date",
        required=True,
        default=fields.Date.today,
        tracking=True,
    )
    date_arrival = fields.Date(
        string="Arrival Declaration Date",
        tracking=True,
        help="Date of the arrival declaration (declaracion de llegada). "
        "Starts the 12-month stay of containers and trailer boxes "
        "(Ley 7547/2025 Art. 14).",
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        store=True,
        help="Ley 7547/2025 Art. 14: 12 months from the import date (raw "
        "materials and inputs), 12 months from the arrival declaration "
        "(containers and trailer boxes), or the program benefit expiry "
        "(other goods).",
    )
    date_extended = fields.Date(
        string="Extended Deadline",
        tracking=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("admitted", "Admitted"),
            ("in_production", "In Production"),
            ("closed", "Closed"),
            ("expired", "Expired"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )
    guarantee_id = fields.Many2one(
        "l10n_py.maquila.guarantee",
        string="Customs Guarantee",
        tracking=True,
    )
    supplier_id = fields.Many2one(
        "res.partner",
        string="Supplier",
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.ref("base.USD"),
    )
    amount_cif = fields.Monetary(
        string="CIF Amount",
    )
    line_ids = fields.One2many(
        "l10n_py.maquila.admission.line",
        "admission_id",
        string="Lines",
    )
    picking_ids = fields.One2many(
        "stock.picking",
        "l10n_py_maquila_admission_id",
        string="Pickings",
    )
    company_id = fields.Many2one(
        related="program_id.company_id",
        store=True,
    )

    @api.constrains("guarantee_id")
    def _check_guarantee_scope(self):
        for rec in self:
            guarantee = rec.guarantee_id
            if (
                guarantee.scope == "operation"
                and len(guarantee._scope_admissions()) > 1
            ):
                raise ValidationError(
                    self.env._(
                        "The guarantee %(guarantee)s is per operation and already "
                        "covers another admission. Use a global guarantee for "
                        "several operations.",
                        guarantee=guarantee.display_name,
                    )
                )

    @api.depends(
        "good_type",
        "date_admission",
        "date_arrival",
        "program_id.benefit_expiry",
    )
    def _compute_date_deadline(self):
        for rec in self:
            deadline = False
            if rec.good_type == "container_box":
                if rec.date_arrival:
                    deadline = rec.date_arrival + relativedelta(months=12)
            elif rec.good_type == "capital_good":
                deadline = rec.program_id.benefit_expiry
            elif rec.date_admission:
                deadline = rec.date_admission + relativedelta(months=12)
            rec.date_deadline = deadline

    def action_admit(self):
        for rec in self:
            if not rec.cnime_certificate:
                raise UserError(
                    self.env._("CNIME certificate is required for admission.")
                )
            if rec.good_type == "container_box" and not rec.date_arrival:
                raise UserError(
                    self.env._(
                        "The arrival declaration date is required to admit "
                        "containers and trailer boxes (Ley 7547/2025 Art. 14)."
                    )
                )
            if rec.guarantee_id:
                guarantee = rec.guarantee_id
                admission_date = rec.date_admission or fields.Date.context_today(rec)
                if (
                    guarantee.state != "active"
                    or guarantee.date_start > admission_date
                    or guarantee.date_end < admission_date
                ):
                    raise UserError(
                        self.env._(
                            "The guarantee %(guarantee)s is not active on the "
                            "admission date (Decreto 5714/2026 Art. 28).",
                            guarantee=guarantee.display_name,
                        )
                    )
                company = rec.company_id or self.env.company
                cif_in_guarantee = rec.currency_id._convert(
                    rec.amount_cif,
                    rec.guarantee_id.currency_id,
                    company,
                    rec.date_admission or fields.Date.context_today(rec),
                )
                if rec.guarantee_id.amount_available < cif_in_guarantee:
                    raise UserError(
                        self.env._(
                            "Insufficient guarantee. Available: %(available)s,"
                            " Required: %(required)s",
                            available=rec.guarantee_id.amount_available,
                            required=cif_in_guarantee,
                        )
                    )
        self.write({"state": "admitted"})

    def action_extend(self):
        """Ley 7547/2025 Art. 14: raw materials and inputs may have their stay
        extended (biministerial resolution) for a period not exceeding the
        original 12 months. Containers and trailer boxes (12 months maximum)
        and the other goods (stay tied to the program) cannot be extended."""
        for rec in self:
            if rec.good_type == "container_box":
                raise UserError(
                    self.env._(
                        "Containers and trailer boxes stay at most 12 months "
                        "from the arrival declaration and cannot be extended "
                        "(Ley 7547/2025 Art. 14)."
                    )
                )
            if rec.good_type == "capital_good":
                raise UserError(
                    self.env._(
                        "These goods may stay while the Maquila program is in "
                        "force; there is no admission deadline to extend "
                        "(Ley 7547/2025 Art. 14)."
                    )
                )
            if rec.state not in ("admitted", "in_production"):
                raise UserError(
                    self.env._("Only admitted goods can have their deadline extended.")
                )
            if rec.date_extended:
                raise UserError(
                    self.env._("This admission has already been extended once.")
                )
            if not rec.date_deadline:
                raise UserError(self.env._("The admission has no deadline to extend."))
            rec.date_extended = rec.date_deadline + relativedelta(months=12)

    def action_in_production(self):
        self.write({"state": "in_production"})

    def action_close(self):
        self.write({"state": "closed"})

    def action_draft(self):
        self.write({"state": "draft"})


class MaquilaAdmissionLine(models.Model):
    _name = "l10n_py.maquila.admission.line"
    _description = "Maquila Admission Line"

    admission_id = fields.Many2one(
        "l10n_py.maquila.admission",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        "product.product",
        required=True,
    )
    lot_id = fields.Many2one(
        "stock.lot",
        string="Lot/Serial",
    )
    quantity = fields.Float(
        required=True,
        digits="Product Unit of Measure",
    )
    uom_id = fields.Many2one(
        "uom.uom",
        string="Unit of Measure",
    )
    ncm_code = fields.Char(
        string="NCM Code",
    )
    currency_id = fields.Many2one(
        related="admission_id.currency_id",
    )
    fob_value = fields.Monetary(
        string="FOB Value",
    )
    qty_consumed = fields.Float(
        compute="_compute_qty_remaining",
        digits="Product Unit of Measure",
    )
    qty_remaining = fields.Float(
        compute="_compute_qty_remaining",
        digits="Product Unit of Measure",
    )

    @api.depends(
        "quantity",
        "uom_id",
        "product_id",
        "admission_id.state",
        "admission_id.date_admission",
        "admission_id.company_id",
    )
    def _compute_qty_remaining(self):
        """Consumed qty is the share of goods that have left the temporary
        admission location, allocated FIFO across the admission lines that
        share the same product and company, ordered by admission date.

        Done with grouped queries (one per recordset) instead of per-line
        searches to avoid an O(n^2) cost."""
        admission_loc = self.env.ref(
            "l10n_py_maquila_ops.stock_location_maquila_admission",
            raise_if_not_found=False,
        )
        products = self.product_id
        companies = self.admission_id.company_id
        # Total outflow per (product, company), in one grouped query.
        out_by_key = {}
        if admission_loc and products and companies:
            groups = self.env["stock.move"]._read_group(
                [
                    ("product_id", "in", products.ids),
                    ("location_id", "=", admission_loc.id),
                    ("state", "=", "done"),
                    ("company_id", "in", companies.ids),
                ],
                groupby=["product_id", "company_id"],
                aggregates=["product_qty:sum"],
            )
            out_by_key = {
                (product.id, company.id): qty for product, company, qty in groups
            }
        # All relevant admission lines, grouped and FIFO-ordered once.
        siblings_by_key = {}
        if products and companies:
            all_lines = self.search(
                [
                    ("product_id", "in", products.ids),
                    ("admission_id.company_id", "in", companies.ids),
                    (
                        "admission_id.state",
                        "in",
                        ("admitted", "in_production", "closed"),
                    ),
                ]
            ).sorted(
                key=lambda sl: (
                    sl.admission_id.date_admission or fields.Date.today(),
                    sl.id,
                )
            )
            for sib in all_lines:
                key = (sib.product_id.id, sib.admission_id.company_id.id)
                siblings_by_key.setdefault(key, []).append(sib)
        for line in self:
            key = (line.product_id.id, line.admission_id.company_id.id)
            remaining_out = out_by_key.get(key, 0.0)
            consumed_ref = 0.0
            for sib in siblings_by_key.get(key, []):
                take = min(sib._quantity_ref_uom(), remaining_out)
                if sib.id == line.id:
                    consumed_ref = take
                    break
                remaining_out = max(0.0, remaining_out - take)
            line.qty_consumed = line._ref_uom_to_line(consumed_ref)
            line.qty_remaining = line.quantity - line.qty_consumed

    def _quantity_ref_uom(self):
        """Line quantity expressed in the product's reference unit of measure."""
        self.ensure_one()
        ref_uom = self.product_id.uom_id
        if self.uom_id and ref_uom:
            return self.uom_id._compute_quantity(self.quantity, ref_uom)
        return self.quantity

    def _ref_uom_to_line(self, qty_ref):
        """Convert a reference-UoM quantity back to this line's unit."""
        self.ensure_one()
        ref_uom = self.product_id.uom_id
        if self.uom_id and ref_uom:
            return ref_uom._compute_quantity(qty_ref, self.uom_id)
        return qty_ref
