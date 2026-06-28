# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from . import models
from openupgradelib import openupgrade_tools


def _insert_account_move_related_document(env):
    cr = env.cr
    if openupgrade_tools.table_exists(cr, "fatturapa_related_document_type"):
        cr.execute("SELECT * FROM fatturapa_related_document_type LIMIT 1")
        if cr.fetchone():
            cr.execute("""
                INSERT INTO account_move_related_document (
                    type, name, "lineRef", invoice_id, invoice_line_id, date,
                    numitem, code, cig, cup
                )
                SELECT
                    type, name, "lineRef", invoice_id, invoice_line_id, date,
                    numitem, code, cig, cup
                FROM fatturapa_related_document_type
            """)


def _l10n_it_edi_related_document_post_init_hook(env):
    _insert_account_move_related_document(env)
