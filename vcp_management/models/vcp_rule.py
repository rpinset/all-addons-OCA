# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import json
import logging
from subprocess import check_output

import pathspec

from odoo import fields, models
from odoo.fields import Command

_logger = logging.getLogger(__name__)


class VcpRule(models.Model):
    _name = "vcp.rule"
    _description = "Processing Rule"

    name = fields.Char(required=True)
    branch_pattern = fields.Char(default=".*", required=True)
    active = fields.Boolean(default=True)
    paths = fields.Text(
        help="Define with pathspec especification",
        default="*",
        required=True,
    )
    rule_type = fields.Selection(
        [
            ("cloc", "Cloc Analysis"),
        ],
        required=True,
        default="cloc",
    )

    def _process_rule(self, record, parameters=None):
        """
        Process the rule on the given repository and branch.
        It will call the corresponding method based on the rule type.
        """
        return getattr(self, f"_process_rule_{self.rule_type}")(record, parameters)

    def _process_rule_cloc(self, record, parameters=None):
        """
        Process the rule as a cloc analysis.
        """
        record._download_code()
        if parameters is None:
            parameters = {}
        if "cloc" in parameters:
            cloc_response = parameters["cloc"]
        else:
            cloc_response = self._call_cloc_command(record.local_path)
            parameters["cloc"] = cloc_response
        matches = self._cloc_get_matches(record.local_path)
        cloc_data = self._action_analysis_process_cloc(
            record.local_path, matches, cloc_response
        )
        vals = self._prepare_analysis_rule_info_vals(record, cloc_data)
        if vals["scanned_files"] == 0:
            return False
        analysis_rule_item = record.rule_information_ids.filtered(
            lambda x: x.rule_id == self
        )
        if analysis_rule_item:
            analysis_rule_item.write(vals)
        else:
            record.rule_information_ids = [Command.create(vals)]

    def _prepare_analysis_rule_info_vals(self, record, cloc_data):
        """Prepare analysis information values of a rule."""
        return {
            "rule_id": self.id,
            "res_id": record.id,
            "res_model": record._name,
            "code_count": cloc_data["code"],
            "documentation_count": cloc_data["documentation"],
            "empty_count": cloc_data["empty"],
            "scanned_files": len(cloc_data["paths"]),
        }

    def _action_analysis_process_cloc(self, path, matchs, cloc_response):
        """Abstract method to be used in other modules. Values are returned by
        iterating each match if it exists in the (already defined) cloc response."""
        res = {
            "paths": [],
            "code": 0,
            "documentation": 0,
            "empty": 0,
        }
        for match in matchs:
            if path:
                path_item = path + "/" + match
            else:
                path_item = match
            if path_item in cloc_response:
                res_file = cloc_response[path_item]
                res["paths"].append(path_item)
                res["code"] += res_file["code"]
                res["documentation"] += res_file["comment"]
                res["empty"] += res_file["blank"]
        return res

    def _call_cloc_command(self, local_path):
        res = check_output(["cloc", "--by-file", "--json", local_path])
        return json.loads(res)

    def _cloc_get_matches(self, path):
        """
        Get all matches from rule paths (multiple per line allow in rule)
        in a local path
        """
        spec = pathspec.PathSpec.from_lines("gitignore", self.paths.splitlines())
        return list(spec.match_tree_files(path))
