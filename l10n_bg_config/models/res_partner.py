#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import logging

from odoo import Command, _, fields, models
from odoo.exceptions import UserError

from .l10n_bg_config_mixin import (
    generate_encryption_keys,
    generate_key2,
)

_logger = logging.getLogger(__name__)

try:
    import stdnum
    from stdnum.exceptions import (
        InvalidChecksum,
        InvalidComponent,
        InvalidFormat,
        ValidationError,
    )
except ImportError:
    _logger.debug("Cannot `import external dependency python stdnum package`.")


def _l10n_bg_uic_type():
    return [
        ("bg_uic", "BG Unified identification number (BULSTAT)"),
        ("bg_egn", "BG Identification number"),
        ("bg_pnf", "BG Personal number of a foreigner"),
        ("bg_onnra", "BG Official number from the National Revenue Agency"),
        ("bg_crauid", "BG Unique identification code under the CRA"),
        ("bg_non_eu", "BG Non EU Tax administration number"),
        ("eu_vat", "EU Tax administration number"),
    ]


class ResPartner(models.Model):
    _inherit = ["res.partner", "l10n.bg.config.mixin"]
    _name = "res.partner"

    type = fields.Selection(
        selection_add=[
            ("represent", "Company represent/manager"),
            ("agent", "Company agent"),
            ("tax", "Tax agent"),
        ],
        ondelete={"represent": "set null", "agent": "set null", "tax": "set null"},
    )
    l10n_bg_represent_contact_id = fields.Many2one(
        "res.partner",
        string="Representative",
        compute="_compute_l10n_bg_represent_contact_id",
        inverse="_inverse_l10n_bg_represent_contact_id",
        store=True,
    )
    l10n_bg_uic_type = fields.Selection(
        selection=_l10n_bg_uic_type(),
        string="Type of Bulgaria UID",
        help="Choice type of Bulgaria UID.",
    )
    l10n_bg_uic = fields.Char(
        string="Unique identification code",
        help="Unique identification code for the Bulgaria received from trade registry",
    )
    l10n_bg_key = fields.Char(
        "Api Key",
        help="Enter the key to encrypt the data. "
        "If not entered, a random key will be generated.",
    )
    l10n_bg_crypt_key = fields.Binary(
        "Crypt Key",
        attachment=False,
        help="Enter the key to decrypt the data. "
        "If not entered, a random key will be generated.",
    )

    def _uic_get_prefix(self, id_number):
        return "".join(filter(str.istitle, id_number))

    def _uic_get_digits(self, id_number):
        return "".join(filter(str.isdigit, id_number))

    def _uic_set(self, record, uic_type, id_number, country_code, kind):
        record.l10n_bg_uic_type = uic_type
        record.l10n_bg_uic = stdnum.get_cc_module(country_code, kind).compact(id_number)

    def _uic_try_bg_vat(self, record, id_number):
        try:
            if stdnum.get_cc_module("bg", "vat").validate(id_number):
                self._uic_set(record, "bg_uic", id_number, "bg", "vat")
                return True, None
        except InvalidFormat:
            return (
                False,
                _("Invalid format for Bulgarian VAT number: %s") % id_number,
            )
        except InvalidChecksum:
            _logger.info(f"Invalid check sum of {id_number}")
            return (
                False,
                _("Invalid checksum for Bulgarian VAT number: %s") % id_number,
            )
        except ValidationError as e:
            _logger.info(f"Invalid {id_number} with error {e}")
            return (
                False,
                _("Validation error for Bulgarian VAT: %(vat)s - %(error)s")
                % {"vat": id_number, "error": str(e)},
            )
        return False, None

    def _uic_try_eu_vat(self, record, id_number):
        try:
            if stdnum.get_cc_module("eu", "vat").validate(id_number):
                self._uic_set(record, "eu_vat", id_number, "eu", "vat")
                return True
        except (InvalidComponent, InvalidFormat) as e:
            _logger.debug("Invalid EU VAT %s: %s", id_number, e)
        except ValidationError as e:
            _logger.info(f"Invalid {id_number} with error {e}")
        return False

    def _uic_try_egn(self, record, id_number):
        try:
            if stdnum.get_cc_module("bg", "egn").validate(id_number):
                self._uic_set(record, "bg_egn", id_number, "bg", "egn")
                return True
        except (InvalidFormat, ValidationError) as e:
            _logger.info(f"Invalid EGN {id_number} with error {e}")
        return False

    def _uic_try_pnf(self, record, id_number):
        try:
            if stdnum.get_cc_module("bg", "pnf").validate(id_number):
                self._uic_set(record, "bg_pnf", id_number, "bg", "pnf")
                return True
        except (InvalidFormat, ValidationError) as e:
            _logger.info(f"Invalid PNF {id_number} with error {e}")
        return False

    def _uic_set_non_eu(self, record):
        record.l10n_bg_uic_type = "bg_non_eu"
        record.l10n_bg_uic = "99999999999"

    def _validate_l10n_bg_uic(self, raise_on_error=False):
        """
        Валидира UIC номера за български партньори.

        :param raise_on_error: Ако е True, вдига UserError при невалиден VAT
        :return: True ако валидацията е успешна, False в противен случай
        """
        for record in self:
            id_number = str(record.vat).upper() if record.vat else ""

            # Празен VAT е валиден случай - не всички партньори имат VAT
            if not id_number:
                # Изчистваме старите данни за UIC ако VAT е изтрит
                if record.l10n_bg_uic or record.l10n_bg_uic_type:
                    record.l10n_bg_uic = False
                    record.l10n_bg_uic_type = False
                return True

            validate = False
            error_message = None
            prefix = self._uic_get_prefix(id_number)

            # First, check id numbers with a prefix
            if prefix:
                # BG VAT number convert to uic
                if prefix == "BG":
                    validate, error_message = self._uic_try_bg_vat(record, id_number)

                #  Try for EU VAT Number
                if not validate and not error_message:
                    validate = self._uic_try_eu_vat(record, id_number)

            # After check for EGN and PNF
            if not validate and not prefix and self._uic_get_digits(id_number):
                #  Check for EGN
                validate = self._uic_try_egn(record, id_number)

                # Check for PNF
                if not validate:
                    validate = self._uic_try_pnf(record, id_number)

            # Finally, mark like outside EU if isn't validated
            if not validate:
                if raise_on_error and error_message:
                    raise UserError(error_message)
                self._uic_set_non_eu(record)
                # Не изтриваме VAT, само маркираме като non-EU

        return True

    def _compute_l10n_bg_represent_contact_id(self):
        for record in self:
            l10n_bg_represent_contact_id = record.child_ids.filtered(
                lambda r: r.type == "represent"
            )
            if len(l10n_bg_represent_contact_id) > 1:
                l10n_bg_represent_contact_id = l10n_bg_represent_contact_id[0]

            record.l10n_bg_represent_contact_id = l10n_bg_represent_contact_id

    def _inverse_l10n_bg_represent_contact_id(self):
        for record in self:
            if record.l10n_bg_represent_contact_id:
                record.l10n_bg_represent_contact_id.type = "represent"
                record.child_ids = [
                    Command.link(record.l10n_bg_represent_contact_id.id)
                ]
            else:
                record.l10n_bg_represent_contact_id = False
                current_id = record.id
                record.child_ids.filtered(
                    lambda r, _id=current_id: r.id == _id
                ).type = "contact"

    def get_api_key(self):
        l10n_bg_uic = self.l10n_bg_uic or "99999999999"
        return generate_key2(len(l10n_bg_uic))

    def _update_key(self, values):
        if values.get("l10n_bg_key") and (
            self.l10n_bg_uic or values.get("l10n_bg_uic")
        ):
            return base64.b64encode(
                generate_encryption_keys(
                    values.get("l10n_bg_uic") or self.l10n_bg_uic, values["l10n_bg_key"]
                )
            )
        return False

    def write(self, values):
        # Проверка за промяна на parent_id с различен VAT
        if "parent_id" in values and not self.env.context.get("skip_vat_check", False):
            for record in self:
                # Проверяваме дали партньорът има posted счетоводни записи
                posted_moves = self.env["account.move"].search(
                    [("partner_id", "=", record.id), ("state", "=", "posted")], limit=1
                )

                if posted_moves:
                    new_parent = (
                        self.env["res.partner"].browse(values["parent_id"])
                        if values["parent_id"]
                        else False
                    )
                    old_vat = record.vat
                    new_parent_vat = new_parent.vat if new_parent else False

                    # Ако има различни VAT номера, вдигаме грешка
                    if new_parent_vat and old_vat and new_parent_vat != old_vat:
                        raise UserError(
                            _(
                                "You cannot change the parent company for partner "
                                "'%(partner)s' because the parent has a different Tax "
                                "ID. Partner Tax ID: %(partner_tax)s, Parent Tax ID: "
                                "%(parent_tax)s. "
                                "This is not allowed when there are posted accounting "
                                "entries."
                            )
                            % {
                                "partner": record.name,
                                "partner_tax": old_vat,
                                "parent_tax": new_parent_vat,
                            }
                        )

        # Проверка за промяна на VAT преди записване
        if "vat" in values and not self.env.context.get("block_validate", False):
            for record in self:
                old_vat = record.vat
                new_vat = values["vat"]

                # Ако има промяна на VAT и партньорът има свързани транзакции
                if old_vat != new_vat and old_vat and new_vat:
                    # Проверка за съществуващи счетоводни записи
                    posted_moves = self.env["account.move.line"].search(
                        [
                            ("partner_id", "=", record.id),
                            ("move_id.state", "=", "posted"),
                        ],
                        limit=1,
                    )

                    if posted_moves:
                        raise UserError(
                            _(
                                "You cannot change the Tax ID for partner "
                                "'%(partner)s' because there are already posted "
                                "accounting entries. Old Tax ID: %(old_tax)s, "
                                "New Tax ID: %(new_tax)s"
                            )
                            % {
                                "partner": record.name,
                                "old_tax": old_vat,
                                "new_tax": new_vat,
                            }
                        )

        # Актуализиране на криптиращия ключ
        l10n_bg_crypt_key = self._update_key(values)
        if l10n_bg_crypt_key:
            values["l10n_bg_crypt_key"] = l10n_bg_crypt_key

        res = super().write(values)

        # Актуализиране на представител
        if values.get("type") and values["type"] == "represent":
            company_id = self.env["res.company"].search(
                [("partner_id", "=", self.id)], limit=1
            )
            if company_id:
                company_id.l10n_bg_represent_contact_id = self.id
            elif not company_id and self.parent_id:
                self.parent_id.l10n_bg_represent_contact_id = self.id

        # Валидация на UIC след записване
        if "vat" in values and not self.env.context.get("block_validate", False):
            # Използваме нов контекст за да избегнем рекурсия
            self.with_context(block_validate=True)._validate_l10n_bg_uic()

        return res
