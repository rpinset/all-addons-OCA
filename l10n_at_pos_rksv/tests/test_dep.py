# Copyright 2024 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import shutil

from odoo.tests.common import TransactionCase, tagged
from odoo.tools import config

from .common import TestDownloadMixin
from .regcheck.regcheck import RegChecker


@tagged("integration", "-standard", "-at_install", "post_install")
class TestDep(TransactionCase, TestDownloadMixin):
    """Verify the DEP chain of an existing POS configuration.

    The test only runs when ``pos_config_id`` is set in ``odoo.conf``,
    pointing to an installed POS that produced signed orders.
    """

    def test_dep_for_config(self):
        pos_config_id = config.get("pos_config_id")
        if not pos_config_id:
            self.skipTest("pos_config_id not configured")

        pos_config = self.env["pos.config"].browse(int(pos_config_id)).exists()
        self.assertTrue(pos_config, "No pos config found")

        regcheck_dir = self.get_download_path("asign_test")
        shutil.rmtree(regcheck_dir, ignore_errors=True)

        dep_export = pos_config._asign_dep_export()
        self.save_test_data("asign_test/dep.json", dep_export)

        asign_cert = self.env["asign.cert"].search(
            [("serial_hex", "=", pos_config.asign_serial_hex)], limit=1
        )
        self.assertTrue(asign_cert, "No cert found for config")

        regcheck = RegChecker(
            regcheck_dir,
            crypto_config={
                "base64AESKey": pos_config.asign_key,
                "certificateOrPublicKeyMap": {
                    pos_config.asign_serial_hex: {
                        "id": asign_cert.serial_hex,
                        "signatureDeviceType": "CERTIFICATE",
                        "signatureCertificateOrPublicKey": (asign_cert.cert.decode()),
                    },
                },
            },
        )

        self.assertTrue(regcheck.check(), "DEP must be valid")
