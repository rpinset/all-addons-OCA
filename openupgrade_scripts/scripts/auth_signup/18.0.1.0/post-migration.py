# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "auth_signup", "18.0.1.0/noupdate_changes.xml")
    openupgrade.delete_record_translations(
        env.cr,
        "auth_signup",
        ["mail_template_user_signup_account_created", "set_password_email"],
    )
