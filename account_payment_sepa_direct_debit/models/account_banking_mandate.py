# Copyright 2020 Akretion - Alexis de Lattre
# Copyright 2014 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

NUMBER_OF_UNUSED_MONTHS_BEFORE_EXPIRY = 36

logger = logging.getLogger(__name__)


class AccountBankingMandate(models.Model):
    _inherit = "account.banking.mandate"

    format = fields.Selection(
        selection_add=[("sepa_core", "SEPA CORE"), ("sepa_b2b", "SEPA B2B")],
        default="sepa_core",
        ondelete={"sepa_core": "set default", "sepa_b2b": "set default"},
    )
    unique_mandate_reference = fields.Char(size=35)  # cf ISO 20022

    @api.constrains("format", "partner_bank_id")
    def _check_sepa_mandate(self):
        for mandate in self:
            if (
                mandate.format in ("sepa_core", "sepa_b2b")
                and mandate.partner_bank_id
                and mandate.partner_bank_id.acc_type != "iban"
            ):
                raise ValidationError(
                    _(
                        "The SEPA mandate '%(mandate)s' is linked to bank account "
                        "'%(bank_account)s' which is not an IBAN bank account.",
                        mandate=mandate.display_name,
                        bank_account=mandate.partner_bank_id.display_name,
                    )
                )

    def _sdd_mandate_set_state_to_expired(self):
        logger.info("Searching for SDD Mandates that must be set to Expired")
        expire_limit_date = datetime.today() + relativedelta(
            months=-NUMBER_OF_UNUSED_MONTHS_BEFORE_EXPIRY
        )
        expired_mandates = self.search(
            [
                "|",
                ("last_debit_date", "=", False),
                ("last_debit_date", "<=", expire_limit_date),
                ("format", "in", ("sepa_core", "sepa_b2b")),
                ("state", "in", ("valid", "final")),
                ("signature_date", "<=", expire_limit_date),
            ]
        )
        if expired_mandates:
            expired_mandates.write({"state": "expired"})
            for mandate in expired_mandates:
                mandate.message_post(
                    body=_(
                        "Mandate automatically set to expired after %d months "
                        "without use."
                    )
                    % NUMBER_OF_UNUSED_MONTHS_BEFORE_EXPIRY
                )
            logger.info(
                "%d SDD Mandate set to expired: IDs %s"
                % (len(expired_mandates), expired_mandates.ids)
            )
        else:
            logger.info("0 SDD Mandates had to be set to Expired")
