from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr,
        "im_livechat",
        "15.0.1.0/noupdate_changes.xml",
    )
    openupgrade.delete_record_translations(
        env.cr,
        "im_livechat",
        [
            "livechat_email_template",
        ],
    )
