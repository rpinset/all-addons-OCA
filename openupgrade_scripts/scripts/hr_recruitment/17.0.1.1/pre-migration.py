# Copyright 2025 Le Filament (https://le-filament.com)
# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def _fill_sequence_hr_applicant_refuse_reason(cr):
    openupgrade.logged_query(
        cr,
        "ALTER TABLE hr_applicant_refuse_reason ADD COLUMN IF NOT EXISTS sequence int4",
    )
    openupgrade.logged_query(cr, "UPDATE hr_applicant_refuse_reason SET sequence=id")


@openupgrade.migrate(use_env=False)
def migrate(cr, version):
    _fill_sequence_hr_applicant_refuse_reason(cr)
