from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.set_xml_ids_noupdate_value(
        env, "mail_restrict_send_button", ["group_show_send_message_button"], False
    )
