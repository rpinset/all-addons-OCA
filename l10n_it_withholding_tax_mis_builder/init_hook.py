# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo.tools import sql

logger = logging.getLogger(__name__)

WITHHOLDING_FIELDS_DATA = [
    {
        "table": "account_move_line",
        "name": "withholding_tax_credit",
        "type": "float",
        "string": "Credit without Withholding Tax Amount",
        "sql_value": "credit - COALESCE(withholding_tax_amount, 0)",
        "sql_where": "credit <> 0",
    },
    {
        "table": "account_move_line",
        "name": "withholding_tax_debit",
        "type": "float",
        "string": "Debit without Withholding Tax Amount",
        "sql_value": "debit - COALESCE(withholding_tax_amount, 0)",
        "sql_where": "debit <> 0",
    },
]


def pre_init_hook(cr):
    create_withholding_fields(cr)


def create_withholding_fields(cr):
    for field_data in WITHHOLDING_FIELDS_DATA:
        if not sql.column_exists(cr, field_data["table"], field_data["name"]):
            logger.info(
                "Creating and populating field %s.%s",
                field_data["table"],
                field_data["name"],
            )
            sql.create_column(
                cr,
                field_data["table"],
                field_data["name"],
                field_data["type"],
                comment=field_data["string"],
            )
            query = f"""
                UPDATE {field_data["table"]}
                SET {field_data["name"]} = {field_data["sql_value"]}
                WHERE {field_data["sql_where"]}
                """
            # Disable SQL-injection check
            # because parameters are not inserted by the user
            # pylint: disable=sql-injection
            cr.execute(query)
