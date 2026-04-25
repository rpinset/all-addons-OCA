# Copyright 2025 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env["stock.release.channel"].search(
        [
            ("state", "in", ("open", "locked")),
        ]
    ).collect_pickings = True
