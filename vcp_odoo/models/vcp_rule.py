# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import ast
import base64
import copy
import logging
import os
from pathlib import Path

from odoo import fields, models
from odoo.fields import Command
from odoo.modules.module import _DEFAULT_MANIFEST

_logger = logging.getLogger(__name__)


class VcpRule(models.Model):
    _inherit = "vcp.rule"

    rule_type = fields.Selection(
        selection_add=[("odoo_module", "Odoo Module Analysis")],
        ondelete={"odoo_module": "cascade"},
    )
    odoo_module_rule_ids = fields.Many2many(
        "vcp.rule",
        "vcp_rule_odoo_module_rel",
        "rule_id",
        "odoo_module_rule_id",
    )

    def _process_rule_odoo_module(self, record, parameters=None):
        """
        Process the rule as an Odoo module analysis.
        """
        if record._name != "vcp.repository.branch":
            # It doesn't make sense to process this kind of rules outside
            # of a repository branch, as they need the code to be downloaded
            # and analyzed.
            return
        record._download_code()

        manifests = self._cloc_get_matches(record.local_path)
        for manifest in manifests:
            path = record.local_path + "/" + manifest
            module_path, module_name, _manifest_name = path.rsplit("/", 2)
            module_id = self.env["vcp.odoo.module"]._get_odoo_module(module_name)

            vals = self._process_rule_odoo_module_prepare_vals(record, module_id, path)
            module_version = self.env["vcp.odoo.module.version"].search(
                [
                    ("module_id", "=", module_id),
                    ("repository_branch_id", "=", record.id),
                ],
                limit=1,
            )
            if not module_version:
                module_version = self.env["vcp.odoo.module.version"].create(vals)
            else:
                module_version.write(vals)
            for rule in self.odoo_module_rule_ids:
                rule._process_rule(module_version)

    def _load_odoo_module_manifest(self, path):
        manifest = copy.deepcopy(_DEFAULT_MANIFEST)
        with open(path) as f:
            manifest.update(ast.literal_eval(f.read()))
        return manifest

    def _get_odoo_icon_path(self):
        return [
            "static/src/img/icon.svg",
            "static/src/img/icon.jpg",
            "static/src/img/icon.png",
            "static/description/icon.svg",
            "static/description/icon.jpg",
            "static/description/icon.png",
        ]

    def _get_html_description_path(self):
        return [
            "static/description/index.html",
        ]

    def _process_rule_odoo_module_prepare_vals(
        self, repository_branch, module_id, manifest_path
    ):
        manifest = self._load_odoo_module_manifest(manifest_path)
        depends = []
        for dependancy in manifest.get("depends", []):
            depends.append(self.env["vcp.odoo.module"]._get_odoo_module(dependancy))
        icon = False
        for icon_path in self._get_odoo_icon_path():
            if os.path.exists(os.path.join(os.path.dirname(manifest_path), icon_path)):
                with open(
                    os.path.join(os.path.dirname(manifest_path), icon_path), "rb"
                ) as f:
                    icon = base64.b64encode(f.read())
                break
        python_libs = []
        for lib in manifest.get("external_dependencies", {}).get("python", []):
            python_libs.append(
                self.env["vcp.odoo.python.library"]._get_python_library(lib)
            )
        package_bins = []
        for package_bin in manifest.get("external_dependencies", {}).get("bin", []):
            package_bins.append(
                self.env["vcp.odoo.bin.package"]._get_bin_package(package_bin)
            )
        authors = []
        for author in manifest.get("author").split(","):
            authors.append(self.env["vcp.odoo.author"]._get_author(author.strip()))

        maintainers = []
        for maintainer in manifest.get("maintainers", []):
            maintainers.append(
                repository_branch.platform_id.host_id._get_user(maintainer)
            )

        description = False
        for html_description_path in self._get_html_description_path():
            path = Path(os.path.dirname(manifest_path)) / html_description_path
            if path.exists():
                description = path.read_text()
                break
        return {
            "name": manifest.get("name").strip(),
            "module_id": module_id,
            "author_ids": [Command.set(authors)],
            "maintainer_ids": [Command.set(maintainers)],
            "version": manifest.get(
                "version", repository_branch.branch_id.name + ".0.0-dev"
            ),
            "path": manifest_path[len(repository_branch.local_path) :].rsplit("/", 1)[
                0
            ],
            "license": manifest.get("license"),
            "summary": manifest.get("summary"),
            "website": manifest.get("website"),
            "development_status": manifest.get("development_status"),
            "auto_install": manifest.get("auto_install", False),
            "repository_branch_id": repository_branch.id,
            "depends_on_module_ids": [Command.set(depends)],
            "image_1920": icon,
            "python_library_ids": [Command.set(python_libs)],
            "bin_package_ids": [Command.set(package_bins)],
            "description": description,
        }
