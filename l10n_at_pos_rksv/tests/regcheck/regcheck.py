# Copyright 2024 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import json
import logging
import os
import shutil
import subprocess  # noqa: S404 (DEP verification helper, only used in tests)

_logger = logging.getLogger(__name__)


class RegCheckerError(Exception):
    """Base class for RegChecker failures."""


class RegChecker:
    """Wrapper around the ``regkassen-verification`` Java tool.

    Used by the optional integration tests to validate that the produced
    DEP (Datenerfassungsprotokoll) is conformant with the Austrian RKSV
    specification. Requires a JRE to be installed on the host.
    """

    def __init__(
        self,
        check_dir,
        crypto_config=None,
        dep_file="dep.json",
        result_dir="result",
    ):
        self.check_dir = check_dir
        self.crypto_config = crypto_config
        self.dep_file = dep_file
        self.crypto_config_file = os.path.join(self.check_dir, "crypto_config.json")
        self.result_dir = result_dir
        self.checker_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "regkassen-verification-1.1.1",
        )
        self.checker_jar = "regkassen-verification-depformat-1.1.1.jar"
        self.result = None

    def check(self, dep=None):
        """Run the verification tool against the configured DEP file.

        :param dep: optional DEP object to dump before checking.
        :returns: ``True`` if verification passed.
        """
        if not os.path.exists(self.check_dir):
            os.makedirs(self.check_dir)
            _logger.info("Created check directory %s", self.check_dir)

        with open(self.crypto_config_file, "w", encoding="utf-8") as fp:
            json.dump(self.crypto_config, fp, indent=4, sort_keys=True)

        dep_path = (
            os.path.join(self.check_dir, self.dep_file)
            if not os.path.isabs(self.dep_file)
            else self.dep_file
        )

        if dep:
            with open(dep_path, "w", encoding="utf-8") as fp:
                json.dump(dep, fp, indent=4, sort_keys=True)

        result_path = os.path.join(self.check_dir, self.result_dir)
        if os.path.exists(result_path):
            shutil.rmtree(result_path)
        os.makedirs(result_path)

        if not os.path.exists(self.checker_path):
            raise RegCheckerError(f"Could not find checker at {self.checker_path}")

        cmd = [
            "java",
            (
                "-Xmx100m -XX:ReservedCodeCacheSize=64m "
                "-XX:-UseCompressedClassPointers -Xss256k"
            ),
            "-jar",
            self.checker_jar,
            "-v",
            "-f",
            "-i",
            dep_path,
            "-c",
            self.crypto_config_file,
            "-o",
            result_path,
        ]
        res = subprocess.call(  # noqa: S602 (controlled inputs from tests only)
            " ".join(cmd), shell=True, cwd=self.checker_path
        )

        with open(
            os.path.join(result_path, "DEP-global.json"),
            encoding="utf-8",
        ) as fp:
            self.result = json.load(fp)

        return res == 0 and self.result["verificationState"] == "PASS"
