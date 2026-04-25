# Copyright 2024 Viindoo Technology Joint Stock Company (Viindoo)
# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "website_slides", "17.0.2.7/noupdate_changes.xml")
    openupgrade.delete_record_translations(
        env.cr,
        "website_slides",
        ["mail_notification_channel_invite", "mail_template_slide_channel_invite"],
    )
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "website_slides.rule_slide_channel_not_website",
            "website_slides.rule_slide_slide_not_website",
        ],
    )
