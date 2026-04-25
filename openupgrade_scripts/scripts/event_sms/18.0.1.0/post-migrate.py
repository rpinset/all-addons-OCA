# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "event_sms", "18.0.1.0/noupdate_changes.xml")
    openupgrade.delete_record_translations(
        env.cr, "event_sms", ["sms_template_data_event_reminder"]
    )
