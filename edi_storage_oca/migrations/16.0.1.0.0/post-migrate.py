# Copyright 2024 Camptocamp SA (http://www.camptocamp.com)
# Copyright 2024 Dixmit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
import logging

from openupgradelib import openupgrade

from odoo.addons.http_routing.models.ir_http import slugify

_logger = logging.getLogger(__name__)


def _get_storage_vals(code, record):
    protocol = "odoofs"
    options = record
    if record["backend_type"] == "filesystem":
        protocol = "file"
        options = {}

    if record["backend_type"] == "ftp":
        protocol = "ftp"
        options = {
            "host": record["ftp_server"],
            "port": record["ftp_server"],
            "username": record["ftp_login"],
            "password": record["ftp_password"],
        }
    if record["backend_type"] == "sftp":
        protocol = "sftp"
        options = {
            "host": record["sftp_server"],
            "port": record["sftp_port"],
        }
        if record["sftp_auth_method"] == "pwd":
            options.update(
                {
                    "username": record["sftp_login"],
                    "password": record["sftp_password"],
                }
            )
        elif record["sftp_auth_method"] == "ssh_key":
            _logger.warning(
                "SSH Key requires a PrivateKey file, but we are "
                "providing a string. Please check the migration."
            )
            options.update(
                {
                    "pkey": record["sftp_private_key"],
                }
            )
    if record["backend_type"] == "s3":
        protocol = "s3"
        options = {
            "endpoint_url": record["aws_host"],
            "key": record["aws_access_key_id"],
            "secret": record["aws_secret_access_key"],
        }
    return {
        "name": record["name"],
        "code": code,
        "protocol": protocol,
        "options": json.dumps(options, default=str),
        "directory_path": record.get("directory_path", "."),
    }


@openupgrade.migrate()
def migrate(env, version):
    # make sure all backend_type can be mapped even if corresponding modules
    # have not been migrated (on purpose because we should switch to fs_storage)
    env.cr.execute(
        """
    SELECT * FROM storage_backend
    WHERE id in (SELECT storage_id FROM edi_backend WHERE storage_id IS NOT NULL)
    """
    )
    storage_field = openupgrade.get_legacy_name("storage_id")
    column_names = [desc[0] for desc in env.cr.description]
    storage_backend_records = []
    for row in env.cr.fetchall():
        storage_backend_records.append(dict(zip(column_names, row)))
    fs_storage = env["fs.storage"]

    for record in storage_backend_records:
        defaults = json.loads(record.pop("server_env_defaults"))
        for key in defaults:
            record[key.split("_env_default")[0]] = defaults[key]
        code = slugify(record.get("name")).replace("-", "_")
        if fs_storage.search([("code", "=", code)]):
            code = "%s_%d" % (code, record.id)

        res_id = fs_storage.create(_get_storage_vals(code, record))

        env.cr.execute(
            f"UPDATE edi_backend SET {storage_field} = %s WHERE storage_id = %s",
            (res_id.id, record["id"]),
        )
