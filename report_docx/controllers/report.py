# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

import json
import logging

from jinja2 import exceptions as jinja2_exceptions

from odoo import http, tools

from odoo.addons.web.controllers import report

_logger = logging.getLogger(__name__)


class ReportController(report.ReportController):
    @http.route(["/report_docx"], type="http", auth="user")
    def report_docx(self, report_name, ids=None, context=None, data=None, **kwargs):
        ids = ids and json.loads(ids) or []
        data = data and json.loads(data) or {}
        try:
            docx, ext = (
                http.request.env["ir.actions.report"]
                .with_context(**(context and json.loads(context) or {}))
                ._render_docx(report_name, ids, data=data)
            )
        except jinja2_exceptions.TemplateError as e:
            _logger.exception("Error while generating report %s", report_name)
            return http.request.make_response(
                tools.html_escape(
                    json.dumps(
                        {
                            "code": 200,
                            "message": e.message,
                            "data": http.serialize_exception(e),
                        }
                    )
                )
            )
        except Exception as e:
            _logger.exception("Error while generating report %s", report_name)
            return http.request.make_response(
                tools.html_escape(
                    json.dumps(
                        {
                            "code": 200,
                            "message": "Odoo Server Error",
                            "data": http.serialize_exception(e),
                        }
                    )
                )
            )

        report = http.request.env["ir.actions.report"]._get_report(report_name)
        filename = report._render_docx_filename(report, ids, data, ext)

        return http.request.make_response(
            docx,
            headers=[
                (
                    "Content-Type",
                    "application/zip"
                    if ext == "zip"
                    else (
                        "application/vnd.openxmlformats-officedocument"
                        ".wordprocessingml.document"
                    ),
                ),
                ("Content-Length", len(docx)),
                ("Content-Disposition", http.content_disposition(filename)),
            ],
        )
