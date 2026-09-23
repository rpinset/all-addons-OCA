# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models
from odoo.tools import SQL


class VCPManagementReport(models.Model):
    _name = "vcp.management.report"
    _description = "VCP Statistics"
    _auto = False
    _log_access = False
    _rec_name = "user_id"
    _order = "date desc"

    platform_id = fields.Many2one("vcp.platform")
    user_id = fields.Many2one("vcp.user")
    organization_id = fields.Many2one("vcp.organization")
    repository_id = fields.Many2one("vcp.repository")
    date = fields.Datetime()
    merged_pr_count = fields.Integer()
    created_pr_count = fields.Integer()
    review_count = fields.Integer()
    comment_count = fields.Integer()

    def _get_table_definition(self):
        return {
            "created_prs": {
                "table": "vcp_request",
                "date": "t.created_at",
                "created_pr_count": "1",
            },
            "merged_prs": {
                "table": "vcp_request",
                "date": "t.closed_at",
                "merged_pr_count": "1",
                "filter": "t.is_merged = True",
            },
            "reviews": {
                "table": "vcp_review",
                "date": "t.submitted_at",
                "review_count": "1",
            },
            "comments": {
                "table": "vcp_comment",
                "date": "t.created_at",
                "comment_count": "1",
            },
        }

    @property
    def _table_query(self) -> SQL:
        return SQL(self._get_sql_definition())

    def _get_sql_definition(self):
        definition = self._get_table_definition().items()
        union_queries = []
        element_number = 0
        for table_name, table_def in definition:
            union_queries.append(
                self._get_table_query(
                    table_name, table_def, element_number, len(definition)
                )
            )
            element_number += 1
        return " UNION ALL ".join(union_queries)

    def _get_table_query(self, table_name, table_def, element_number, total_elements):
        from_definition = self._get_from_definition(table_name, table_def)
        select_fields = self._get_select_fields(
            table_def, element_number, total_elements
        )
        select_fields_str = ", ".join(select_fields)
        filter_condition = (
            f"WHERE {table_def['filter']}" if "filter" in table_def else ""
        )
        return f"""
            SELECT
                {select_fields_str}
            FROM {from_definition}
            {filter_condition}
        """

    def _get_from_definition(self, table_name, table_def):
        table = table_def.get("table", table_name)
        repository_id = table_def.get("repository_id", "t.repository_id")
        return f"{table} AS t LEFT JOIN vcp_repository AS r ON {repository_id} = r.id"

    def _get_select_fields(self, table_def, element_number, total_elements):
        organization = table_def.get("organization_id", "t.organization_id")
        return [
            f"{element_number}+{total_elements}*t.id AS id",
            f"{table_def.get('platform_id', 'r.platform_id')} AS platform_id",
            f"{organization} AS organization_id",
            f"{table_def.get('user_id', 't.user_id')} AS user_id",
            f"{table_def.get('repository_id', 't.repository_id')} AS repository_id",
            f"{table_def.get('date', 't.create_date')} AS date",
            f"{table_def.get('merged_pr_count', 0)} AS merged_pr_count",
            f"{table_def.get('created_pr_count', 0)} AS created_pr_count",
            f"{table_def.get('review_count', 0)} AS review_count",
            f"{table_def.get('comment_count', 0)} AS comment_count",
        ]
