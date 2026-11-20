# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import uuid

from odoo import SUPERUSER_ID, api


def get_or_create(record):
    # otro cursor: el rollback del error que ve el usuario no puede perderla
    if not record:
        return str(uuid.uuid4())
    key = record.sudo().l10n_py_sifende_event_key
    if not key:
        key = str(uuid.uuid4())
        _write(record, key, committed=True)
    return key


def forget(record, committed):
    if record and record.sudo().l10n_py_sifende_event_key:
        _write(record, False, committed)


def _write(record, key, committed):
    values = {"l10n_py_sifende_event_key": key}
    if not committed:
        record.sudo().write(values)
        return
    with record.pool.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        env[record._name].browse(record.id).write(values)
    record.invalidate_recordset(list(values))
