# Copyright 2024 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


def uninstall_hook(env):
    for export in env["sql.export"].search([]):
        export._export_delta_cleanup(keep_last=False)
