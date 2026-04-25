from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "crm", "18.0.1.8/noupdate_changes.xml")
