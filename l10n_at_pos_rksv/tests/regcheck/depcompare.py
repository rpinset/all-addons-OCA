#!/usr/bin/env python3
# Copyright 2024 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import argparse
import json
import logging
import os

_logger = logging.getLogger(__name__)


class DepCompare:
    """Compare two DEP (Datenerfassungsprotokoll) files or directories."""

    def load(self, path):
        """Load a single DEP JSON or merge all JSON files of a directory."""
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as fp:
                return json.load(fp)

        files = sorted(
            os.path.join(path, name)
            for name in os.listdir(path)
            if os.path.isfile(os.path.join(path, name)) and name.endswith(".json")
        )
        rows = []
        dep = {
            "Belege-Gruppe": [
                {
                    "Signaturzertifikat": "",
                    "Zertifizierungsstellen": [],
                    "Belege-kompakt": rows,
                }
            ]
        }
        for dep_path in files:
            with open(dep_path, encoding="utf-8") as dep_file:
                partly_dep = json.load(dep_file)
                rows += partly_dep["Belege-Gruppe"][0]["Belege-kompakt"]
        return dep

    def compare_obj(self, obj1, obj2):
        return json.dumps(obj1, indent=4, sort_keys=True) == json.dumps(
            obj2, indent=4, sort_keys=True
        )

    def compare(self, path1, path2):
        return self.compare_obj(self.load(path1), self.load(path2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="DEP Protocol Compare/Checker")
    parser.add_argument("path1", help="First Source File/Directory")
    parser.add_argument("path2", help="Second Source File/Directory")
    args = parser.parse_args()

    if DepCompare().compare(args.path1, args.path2):
        _logger.info("Files are EQUAL")
    else:
        _logger.error("Files are NOT equal")
