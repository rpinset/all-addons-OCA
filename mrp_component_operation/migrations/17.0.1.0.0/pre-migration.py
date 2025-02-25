# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    field_spec = [
        (
            "mrp_component_operation",
            "mrp_component_operation",
            "source_location_id",
            "manufacture_location_id",
        ),
    ]
    openupgrade.rename_fields(env=env, field_spec=field_spec, no_deep=True)
