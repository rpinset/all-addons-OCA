# l10n_py_base/validators/ruc_validator.py

"""RUC validation helpers for Paraguay.

The check digit is computed by ``python-stdnum`` (``stdnum.py.ruc``), which
implements the modulo 11 algorithm published by the SET and is already used by
``base_vat`` for Paraguayan partners.
"""

import logging

from stdnum.exceptions import (
    InvalidChecksum,
    InvalidFormat,
    InvalidLength,
    ValidationError,
)
from stdnum.py import ruc as stdnum_ruc

_logger = logging.getLogger(__name__)

# A RUC has at most 9 digits, the last one being the check digit.
MAX_RUC_LENGTH = 9


class RUCValidator:
    """Validate and format Paraguayan RUC numbers."""

    @classmethod
    def validate(cls, ruc):
        """Validate a full RUC, check digit included.

        Args:
            ruc (str): RUC to validate, with or without the dash.

        Returns:
            tuple: (is_valid, error_message)
        """
        if not ruc:
            return False, "RUC is required."

        number = stdnum_ruc.compact(ruc)
        try:
            stdnum_ruc.validate(number)
        except InvalidFormat:
            return False, "Invalid RUC format. Use: NNNNNNNN-D or NNNNNNNND"
        except InvalidLength:
            return (
                False,
                f"A RUC has at most {MAX_RUC_LENGTH} digits, "
                "including the check digit.",
            )
        except InvalidChecksum:
            expected = stdnum_ruc.calc_check_digit(number[:-1])
            return (
                False,
                f"Invalid check digit. Expected: {expected}, "
                f"received: {number[-1]}",
            )
        except ValidationError:
            return False, "Invalid RUC."

        return True, ""

    @classmethod
    def _calculate_check_digit(cls, ruc_number):
        """Return the check digit for a RUC given without it.

        Args:
            ruc_number (str): RUC number without the check digit.

        Returns:
            int: check digit computed with the SET modulo 11 algorithm.
        """
        number = stdnum_ruc.compact(ruc_number or "")
        return int(stdnum_ruc.calc_check_digit(number))

    @classmethod
    def format_ruc(cls, ruc, include_dv=True):
        """Format a RUC as ``NNNNNNNN-D``.

        A number that already carries a valid check digit is only reformatted.
        Otherwise the whole number is taken as the base and the check digit is
        computed.

        Args:
            ruc (str): RUC in any format.
            include_dv (bool): whether to return the check digit as well.

        Returns:
            str: formatted RUC, or the original value when it is not numeric.
        """
        number = stdnum_ruc.compact(ruc or "")
        if not number.isdigit():
            return ruc

        if stdnum_ruc.is_valid(number):
            base, check_digit = number[:-1], number[-1]
        else:
            base, check_digit = number, stdnum_ruc.calc_check_digit(number)

        return f"{base}-{check_digit}" if include_dv else base

    @classmethod
    def get_ruc_number(cls, ruc):
        """Return the RUC without its check digit.

        Numbers whose check digit does not match are returned unchanged, since
        no assumption can be made about which part is the base.
        """
        number = stdnum_ruc.compact(ruc or "")
        if not number.isdigit():
            return ""
        return number[:-1] if stdnum_ruc.is_valid(number) else number

    @classmethod
    def get_check_digit(cls, ruc):
        """Return the check digit of a RUC as a string."""
        return str(cls._calculate_check_digit(cls.get_ruc_number(ruc)))

    @classmethod
    def is_valid_format(cls, ruc):
        """Check the shape of a RUC without validating the check digit."""
        if not ruc:
            return False

        number = stdnum_ruc.compact(ruc)
        return number.isdigit() and 2 <= len(number) <= MAX_RUC_LENGTH

    @classmethod
    def normalize(cls, ruc):
        """Return the RUC in the standard ``NNNNNNNN-D`` presentation."""
        if not ruc:
            return ""

        is_valid, error = cls.validate(ruc)
        if not is_valid:
            _logger.warning("Invalid RUC: %s - %s", ruc, error)
            return ruc

        return stdnum_ruc.format(ruc)
