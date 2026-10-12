# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
"""Backfill ``l10n_py_iva_affectation`` for pre-existing account.tax rows.

The field ``account.tax.l10n_py_iva_affectation`` was added with
``default="1"`` (Gravado IVA). When this column was first added to an
existing database, Odoo's own schema sync backfills that default onto
every pre-existing row where the column is still NULL -- including
taxes that were already configured with ``amount == 0`` (Exenta /
Exonerado), which then get silently reported as ``ivaTipo=1`` (Gravado)
in the SIFEN electronic document, instead of the correct Exenta value.

This mirrors, for existing data, the exact same heuristic
``l10n_py_edi_base``'s own runtime fallback
(``AccountMove._l10n_py_infer_affectation``) already uses for taxes
that have no explicit affectation: ``amount == 0`` implies Exenta
("3"). It intentionally does NOT attempt to distinguish Exenta ("3")
from Exonerado ("2") -- that distinction cannot be inferred from
``amount`` alone, and guessing it wrong would be worse than leaving it
as Exenta (both are non-taxed for the ``dPropIVA`` calculation; only
the ``iAfecIVA`` code itself differs, and Exenta is the more common
case in practice). A consultant must explicitly reclassify a tax as
Exonerado when that applies.
"""


def migrate(cr, version):
    cr.execute(
        """
        UPDATE account_tax
           SET l10n_py_iva_affectation = '3'
         WHERE l10n_py_iva_affectation = '1'
           AND amount = 0
        """
    )
