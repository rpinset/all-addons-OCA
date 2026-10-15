# Copyright 2025 Camptocamp SA (https://www.camptocamp.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
import logging

_logger = logging.getLogger(__name__)

OPTION = "allow_ignore_expiration_date"
SCENARIO_XMLIDS = ("shopfloor.scenario_location_content_transfer",)


def _get_scenarios(env):
    """Return the scenarios supporting the option."""
    scenarios = env["shopfloor.scenario"]
    for xmlid in SCENARIO_XMLIDS:
        scenarios |= env.ref(xmlid, raise_if_not_found=False) or scenarios.browse()
    return scenarios


def post_init_hook(env):
    """Enable the ignore expiration date option on supported scenarios."""
    for scenario in _get_scenarios(env):
        _logger.info("Add %s option on %s scenario", OPTION, scenario.key)
        options = scenario.options
        options[OPTION] = True
        scenario.options_edit = json.dumps(options)


def uninstall_hook(env):
    """Remove the ignore expiration date option from supported scenarios."""
    for scenario in _get_scenarios(env):
        _logger.info("Remove %s option from %s scenario", OPTION, scenario.key)
        options = scenario.options
        options.pop(OPTION, None)
        scenario.options_edit = json.dumps(options)
