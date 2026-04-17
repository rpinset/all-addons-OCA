# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

import functools
import inspect
import io
from base64 import b64decode
from collections import namedtuple
from zipfile import ZipFile

from docxtpl import DocxTemplate
from jinja2 import Environment as Environment_jinja2, StrictUndefined
from markupsafe import Markup

from odoo import _, api, fields, models, tools
from odoo.tools.safe_eval import safe_eval, time

try:
    from num2words import num2words
except ImportError:

    def num2words(*args, **kwargs):
        return args[0]


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    report_type = fields.Selection(
        selection_add=[("docx", "DOCX")], ondelete={"docx": "cascade"}
    )
    docx_template = fields.Binary("Template", attachment=True)
    docx_template_filename = fields.Char(compute="_compute_docx_template_filename")
    docx_multi_mode = fields.Selection(
        [("zip", "Zip file"), ("template", "Template")],
        string="Multi records",
        help="Select the behavior when the user selected multiple records",
        default="zip",
    )
    docx_expression_test_model_id = fields.Many2one(
        "ir.model", compute="_compute_docx_expression_test_model_id"
    )
    docx_expression_test_record = fields.Reference(
        selection=lambda self: self.env["ir.model"]
        .search([])
        .mapped(lambda x: (x.model, x.name)),
        string="Record",
        store=False,
    )
    docx_expression_test_expression = fields.Char("Test expression", store=False)
    docx_expression_test_result = fields.Char(
        "Result", compute="_compute_docx_expression_test", store=False
    )
    docx_expression_test_code = fields.Char(
        "Code", compute="_compute_docx_expression_test", store=False
    )
    docx_help = fields.Html(compute="_compute_docx_help")

    def _compute_docx_template_filename(self):
        for this in self:
            this.docx_template_filename = _("template.docx")

    @api.depends("model")
    def _compute_docx_expression_test_model_id(self):
        for this in self:
            this.docx_expression_test_model_id = (
                self.env["ir.model"]._get(this.model).id
            )

    @api.depends(
        "docx_expression_test_record", "docx_expression_test_expression", "model"
    )
    def _compute_docx_expression_test(self):
        for this in self:
            if (
                this.docx_expression_test_record
                and this.docx_expression_test_expression
            ):
                try:
                    template_code = "{{ " + this.docx_expression_test_expression + " }}"
                    this.docx_expression_test_result = (
                        Environment_jinja2(undefined=StrictUndefined)
                        .from_string(template_code)
                        .render(
                            self._render_docx_eval_context(
                                self, this.docx_expression_test_record.ids, {}
                            )
                        )
                    )
                    this.docx_expression_test_code = template_code
                except Exception as e:
                    this.docx_expression_test_result = getattr(e, "message", str(e))
                    this.docx_expression_test_code = False
            else:
                this.docx_expression_test_result = _(
                    "Select a record and fill in an expression"
                )
                this.docx_expression_test_code = False

    @api.depends("docx_multi_mode", "docx_expression_test_record")
    def _compute_docx_help(self):
        for this in self:
            this.docx_help = self.env["ir.qweb"]._render(
                "report_docx.template_help", {"object": this}
            )

    @api.onchange("docx_template_filename")
    def _onchange_docx_template_filename(self):
        if not self.report_name:
            self.report_name = self.docx_template_filename

    def _render_docx(self, report_ref, res_ids, data=None):
        report = self._get_report(report_ref)
        if report.docx_multi_mode == "zip" and len(res_ids) > 1:
            zip_buffer = io.BytesIO()
            with ZipFile(zip_buffer, "a") as zip_file:
                for res_id in res_ids:
                    docx, ext = self._render_docx(report_ref, [res_id], data=data)
                    zip_file.writestr(
                        self._render_docx_filename(report, [res_id], data, ext),
                        docx,
                    )
            return zip_buffer.getvalue(), "zip"
        template = DocxTemplate(io.BytesIO(b64decode(report.docx_template)))
        template.render(self._render_docx_eval_context(report, res_ids, data))
        result = io.BytesIO()
        template.save(result)
        return result.getvalue(), "docx"

    def _render_docx_eval_context(self, report, res_ids, data):
        result = self._get_rendering_context(report, res_ids, data)
        result["html2plaintext"] = tools.html2plaintext
        result["num2words"] = functools.partial(
            num2words, lang=self.env.context.get("lang") or "en"
        )
        result["object"] = result["docs"][:1]
        result["o"] = result["docs"][:1]
        result.update(**self.env["mail.render.mixin"]._render_eval_context())
        return result

    def _render_docx_filename(self, report, res_ids, data, ext):
        filename = report.report_name

        if len(res_ids) == 1 and report.print_report_name:
            filename = safe_eval(
                report.print_report_name,
                {"object": self.env[report.model].browse(res_ids), "time": time},
            )

        if not filename.endswith(f".{ext}"):
            filename += f".{ext}"

        return filename

    def _docx_help_get_scope(self):
        self.ensure_one()
        if not self.docx_expression_test_record:
            return []
        ScopeItem = namedtuple("ScopeItem", ["name", "explanation"])
        result = []
        explanations = self._docx_help_get_explanations()
        for key, value in self._render_docx_eval_context(
            self, self.docx_expression_test_record.ids, {}
        ).items():
            explanation = explanations.get(key)
            if explanation == "hide":
                continue
            if inspect.isfunction(value):
                key = key + str(inspect.signature(value))
            result.append(ScopeItem(key, explanation))
        return sorted(result, key=lambda x: x[0])

    def _docx_help_get_explanations(self):
        return {
            "abs": _("Returns the absolute value of a number"),
            "ctx": "hide",
            "datetime": Markup(
                _(
                    "Python datetime module. Ie <code>datetime.datetime.now()"
                    "</code> returns the current date"
                )
            ),
            "docs": "hide",
            "doc_ids": "hide",
            "doc_model": "hide",
            "filter": "hide",
            "format_amount": Markup(
                _(
                    "Formats an amount according to a currency, usually called like <code>"
                    "format_amount(object.amount_field, object.currency_id)</code>.<br/>"
                    "Note you can format any number according to the company currency by "
                    "using <code>object.env.company.currency_id.format(42)</code>"
                )
            ),
            "format_date": Markup(
                _(
                    "Formats a date according to the current language, ie "
                    "<code>format_date(object.create_date)</code>"
                )
            ),
            "format_datetime": Markup(
                _(
                    "Formats a date and time according to the current language, ie "
                    "<code>format_datetime(object.create_date)</code>"
                )
            ),
            "format_duration": Markup(
                _(
                    "Formats a number as a time interval, ie "
                    "<code>format_duration(1.5)</code> "
                    "returns <code>01:30</code>"
                )
            ),
            "format_time": Markup(
                _(
                    "Formats a time according to the current language, ie "
                    "<code>format_time(object.create_date)</code>"
                )
            ),
            "hasattr": "Checks if some object has an attribute",
            "html2plaintext": "Converts HTML to text",
            "is_html_empty": Markup(
                _(
                    "Checks if an html field is empty, ie "
                    "<code>is_html_empty('&lt;p/&gt;')</code> returns <code>True</code>"
                )
            ),
            "len": "Returns the length of a string or record collection",
            "map": "hide",
            "max": Markup(
                _(
                    "Returns the maximum of the arguments passed. "
                    "<code>max(0, 42, 41)</code> returns <code>42</code>"
                )
            ),
            "min": Markup(
                _(
                    "Returns the minimum of the arguments passed. "
                    "<code>min(0, 42, 41)</code> returns <code>0</code>"
                )
            ),
            "num2words": Markup(
                _(
                    "Converts a number to a string, ie <code>num2words(42)</code> returns "
                    "<code>&quot;fourty-two&quot;</code>"
                )
            ),
            "o": "hide",
            "object": "hide",
            "quote": "hide",
            "reduce": "hide",
            "relativedelta": Markup(
                _(
                    "Python relativedelta module. Allows complex date computations "
                    "like "
                    "<code>datetime.date.today() + relativedelta(months=2, day=1) - "
                    "relativedelta(days=1)</code> which returns the date of the last "
                    "day of the next month"
                )
            ),
            "sum": Markup(
                _(
                    "Sums up the argument collection, ie "
                    "<code>sum(docs.mapped('some_field'))</code> "
                    "returns the sum of the values of <em>some_field</em>"
                )
            ),
            "urlencode": "hide",
            "user": "The user generating the report",
        }
