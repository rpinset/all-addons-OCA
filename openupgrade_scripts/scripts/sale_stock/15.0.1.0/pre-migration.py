from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_columns(env.cr, {"sale_order": [("effective_date", None)]})
    # We need to recreate the column in order to avoid computation of the field.
    # It will be filled on post-migration.
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE sale_order
        ADD COLUMN effective_date timestamp
        """,
    )
