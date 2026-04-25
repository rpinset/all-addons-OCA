from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "hr", "18.0.1.1/noupdate_changes.xml")
    openupgrade.delete_record_translations(
        env.cr, "hr", ["contract_type_part_time"], ["name"]
    )
    openupgrade.delete_records_safely_by_xml_id(env, ["hr.hr_presence_control_login"])
