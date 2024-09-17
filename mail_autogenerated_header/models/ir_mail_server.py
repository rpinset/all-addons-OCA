# Copyright 2018 Therp BV <https://therp.nl>
# Copyright 2022 Hunki Enterprises BV <https://hunki-enterprises.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    @api.model
    def send_email(
        self,
        message,
        mail_server_id=None,
        smtp_server=None,
        smtp_port=None,
        smtp_user=None,
        smtp_password=None,
        smtp_encryption=None,
        smtp_debug=False,
        smtp_session=None,
    ):
        """Inject autogenerated header for autogoing mails"""

        if not self.env.context.get(
            "mail_autogenerated_header_disable"
        ) and self._send_email_set_autogenerated(
            message,
            mail_server_id=mail_server_id,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_password=smtp_password,
            smtp_encryption=smtp_encryption,
            smtp_debug=smtp_debug,
            smtp_session=smtp_session,
        ):
            # MS Exchange's broken version as of
            # http://blogs.technet.com/b/exchange/archive/2006/10/06/
            # 3395024.aspx
            message["Precedence"] = "bulk"
            message["X-Auto-Response-Suppress"] = "OOF"
            # The right way to do it as of
            # https://tools.ietf.org/html/rfc3834
            message["Auto-Submitted"] = "auto-generated"

        return super().send_email(
            message,
            mail_server_id=mail_server_id,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_password=smtp_password,
            smtp_encryption=smtp_encryption,
            smtp_debug=smtp_debug,
            smtp_session=smtp_session,
        )

    @api.model
    def _send_email_set_autogenerated(
        self,
        message,
        mail_server_id=None,
        smtp_server=None,
        smtp_port=None,
        smtp_user=None,
        smtp_password=None,
        smtp_encryption=None,
        smtp_debug=False,
        smtp_session=None,
    ):
        """Determine if some mail should have the autogenerated headers"""

        mail = self.env["mail.mail"].search(
            [
                ("message_id", "=", message["Message-Id"]),
            ]
        )
        if not mail:
            return False
        return mail.subtype_id != self.env.ref("mail.mt_comment")
