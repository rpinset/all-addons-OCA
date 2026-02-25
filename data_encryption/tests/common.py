# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo.tests.common import TransactionCase
from odoo.tools.config import config

_logger = logging.getLogger(__name__)

try:
    from cryptography.fernet import Fernet
except ImportError as err:  # pragma: no cover
    _logger.debug(err)


class CommonDataEncrypted(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.encrypted_data = cls.env["encrypted.data"]
        cls.set_new_key_env("test")
        old_running_env = config.get("running_env", "")

        def reset_running_env():
            config["running_env"] = old_running_env

        cls.addClassCleanup(reset_running_env)
        config["running_env"] = "test"
        cls.crypted_data_name = "test_model,1"

    @classmethod
    def set_new_key_env(cls, environment):
        crypting_key = Fernet.generate_key()
        # The key is encoded to bytes in the module, because in real life
        # the key com from the config file and is not in a binary format.
        # So we decode here to avoid having a special behavior because of
        # the tests.
        encryption_key_environment_config_name = f"encryption_key_{environment}"
        old_key = config.get(encryption_key_environment_config_name, "")

        def reset_config_key():
            config[encryption_key_environment_config_name] = old_key

        cls.addClassCleanup(reset_config_key)
        config[encryption_key_environment_config_name] = crypting_key.decode()
