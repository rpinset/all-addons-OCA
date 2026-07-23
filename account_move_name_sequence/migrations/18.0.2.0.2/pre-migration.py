# Copyright 2025 Le Filament (https://www.le-filament.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """
    This migration script was added for handling made_sequence_gap added in v18
    Openupgrade script initialize this value to True and the recompute it
    based on sequence_number / sequence_prefix
    (see https://github.com/OCA/OpenUpgrade/pull/5447)
    Since these 2 fields are not used by this module (except when journal is in hashed
    mode), we need to force all made_sequence_gap to False when these fields are not set
    """
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_move am
        SET made_sequence_gap = False
        FROM account_journal aj
        WHERE am.journal_id = aj.id
            AND aj.restrict_mode_hash_table IS NOT TRUE
        """,
    )
