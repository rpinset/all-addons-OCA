#!/usr/bin/env python3
"""
Standalone test script for MT940 parser - no Odoo installation needed.
Usage: python3 test_parser_standalone.py <path_to_mt940_file>
"""

import logging
import os
import sys

_logger = logging.getLogger(__name__)

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    import re

    import mt940
    import mt940.tags
except ImportError:
    _logger.info(
        "ERROR: mt-940 library not installed. Install with: pip install mt-940"
    )
    sys.exit(1)

# Apply ProCredit PRCB Statement Number fix (from models/__init__.py)
mt940.tags.StatementNumber.pattern = r"""
    (?P<statement_number>\d+)
    (?:/?(?P<sequence_number>\d{1,6})|
    -(?P<alt_sequence_number>\d{1,6}))?
    $"""


class Tag:
    def parse(self, transactions, value):
        match = re.match(self.pattern, value, self.RE_FLAGS)
        if match:  # pragma: no branch
            return match.groupdict()
        else:  # pragma: no cover
            part_value = value
            for pattern in self.pattern.split("\n"):
                match = re.match(pattern, part_value, self.RE_FLAGS)
                if match:
                    part_value = part_value[len(match.group(0)) :]
                else:
                    pass
            raise RuntimeError(f"Unable to parse {self!r} from {value!r}")
        return match.groupdict()


mt940.tags.Tag.parse = Tag.parse


# Mock the bank_custom_tags module classes
class BankTransactionParser:
    """Base class for parsing bank transaction descriptions in Bulgarian MT940 files."""

    # Common patterns for Bulgarian bank statements
    RECIPIENT_PATTERNS = [
        "ПОЛУЧАТЕЛ:",
        "получател:",
        "Получател:",
    ]
    ACCOUNT_PATTERNS = [
        "СМЕТКА:",
        "сметка:",
        "Сметка:",
    ]
    BIC_PATTERNS = [
        "BIC:",
        "bic:",
        "Bic:",
    ]
    RATE_PATTERNS = [
        "КУРС:",
        "курс:",
        "Курс:",
    ]

    def __init__(self, tag_data, bank_swift_id=None):
        self.tag_data = tag_data
        self.bank_swift_id = bank_swift_id
        self.parsed_data = {}

    def get_version(self):
        return self.bank_swift_id

    def parse(self):
        """Parse transaction description and extract structured data."""
        self.parsed_data = self._extract_common_fields()
        return self.parsed_data

    def _extract_common_fields(self):
        """Extract common fields from transaction description."""
        data = {}

        # Try to extract recipient/partner name
        for pattern in self.RECIPIENT_PATTERNS:
            recipient = self._extract_after_pattern(pattern)
            if recipient:
                data["ПОЛУЧАТЕЛ:"] = recipient
                break

        # Try to extract account number
        for pattern in self.ACCOUNT_PATTERNS:
            account = self._extract_after_pattern(pattern)
            if account:
                data["СМЕТКА:"] = account
                break

        # Try to extract BIC
        for pattern in self.BIC_PATTERNS:
            bic = self._extract_after_pattern(pattern)
            if bic:
                data["BIC:"] = bic
                break

        # Try to extract exchange rate
        for pattern in self.RATE_PATTERNS:
            rate = self._extract_after_pattern(pattern)
            if rate:
                data["КУРС:"] = rate
                break

        return data

    def _extract_after_pattern(self, pattern):
        """Extract text after a pattern until next pattern or end."""
        if pattern not in self.tag_data:
            return None

        # Find the position after the pattern
        start_pos = self.tag_data.find(pattern) + len(pattern)
        remaining_text = self.tag_data[start_pos:]

        # Find the next pattern or end of string
        end_pos = len(remaining_text)
        all_patterns = (
            self.RECIPIENT_PATTERNS
            + self.ACCOUNT_PATTERNS
            + self.BIC_PATTERNS
            + self.RATE_PATTERNS
        )

        for next_pattern in all_patterns:
            if next_pattern == pattern:
                continue
            if next_pattern in remaining_text:
                pos = remaining_text.find(next_pattern)
                if pos < end_pos:
                    end_pos = pos

        result = remaining_text[:end_pos].strip()
        return result if result else None

    def get_data(self):
        """Return parsed data (for backward compatibility)."""
        if not self.parsed_data:
            self.parse()
        return self.parsed_data


def detect_bank_format(account_identification):
    """Detect bank format based on IBAN or BIC codes in the statement."""
    # UBB (ОББ) has BIC starting with UBBS
    if account_identification and "UBBS" in account_identification.upper():
        return "ubb"
    # ProCredit has BIC starting with BUIN or PRCB
    if account_identification and (
        "BUIN" in account_identification.upper()
        or "PRCB" in account_identification.upper()
    ):
        return "procredit"
    # Unicredit Bulbank has BIC starting with UNCR
    if account_identification and "UNCR" in account_identification.upper():
        return "procredit"  # Uses same format as ProCredit
    # Default to ProCredit format for backward compatibility
    return "procredit"


def parse_mt940_file(file_path):
    """Parse MT940 file and return structured data."""
    _logger.info(f"\n{'='*80}")
    _logger.info(f"Parsing MT940 file: {file_path}")
    _logger.info(f"{'='*80}\n")

    # Try different encodings
    encodings = ["utf-8", "windows-1251", "iso-8859-5", "cp1251"]

    for encoding in encodings:
        try:
            _logger.info(f"Trying encoding: {encoding}")
            with open(file_path, "rb") as f:
                data = f.read().decode(encoding)

            # Parse with mt940 library
            transactions = mt940.parse(data)
            _logger.info(f"✓ Successfully parsed with {encoding}\n")

            # Get transaction data
            mt940_transactions_data = transactions.data

            # Detect bank format
            account_identification = mt940_transactions_data.get(
                "account_identification", ""
            )
            bank_format = detect_bank_format(account_identification)

            _logger.info(f"Bank Format: {bank_format}")
            _logger.info(f"Account: {account_identification}")
            _logger.info(
                f"Statement Number: {mt940_transactions_data.get('statement_number')}"
            )
            transaction_reference = mt940_transactions_data.get("transaction_reference")
            _logger.info(f"Transaction Reference: {transaction_reference}")
            _logger.info(
                f"\nOpening Balance: {mt940_transactions_data['final_opening_balance']}"
            )
            _logger.info(
                f"Closing Balance: {mt940_transactions_data['final_closing_balance']}"
            )

            # Parse transactions
            _logger.info(f"\n{'='*80}")
            _logger.info(f"TRANSACTIONS ({len(list(transactions))} total)")
            _logger.info(f"{'='*80}\n")

            for idx, transaction in enumerate(transactions, 1):
                if not transaction:
                    continue

                trans_data = transaction.data
                _logger.info(f"\n--- Transaction #{idx} ---")
                _logger.info(f"Date: {trans_data['date']}")
                _logger.info(f"Amount: {trans_data['amount']}")
                _logger.info(
                    f"Customer Reference: {trans_data.get('customer_reference', 'N/A')}"
                )
                _logger.info(f"Transaction ID: {trans_data.get('id', 'N/A')}")

                # Parse transaction details
                transaction_details = trans_data.get("transaction_details", "")
                if transaction_details:
                    _logger.info("\nRaw Transaction Details:")
                    _logger.info(
                        f"{transaction_details[:200]}..."
                        if len(transaction_details) > 200
                        else transaction_details
                    )

                    # Parse details based on bank format
                    if bank_format == "ubb":
                        _logger.info("\n[UBB Format - // separator]")
                        parts = transaction_details.split("//")
                        for i, part in enumerate(parts[:5]):  # Show first 5 parts
                            _logger.info(f"  Part {i}: {part[:80]}")
                    else:
                        # ProCredit/UniCredit format
                        separator = "^" if "^" in transaction_details else "+"
                        _logger.info(
                            f"\n[ProCredit/UniCredit Format - '{separator}' separator]"
                        )
                        parts = transaction_details.split(separator)

                        for part in parts[:10]:  # Show first 10 parts
                            part = part.strip()
                            if part:
                                # Check if it's a numbered field
                                if part[:2].isdigit():
                                    field_num = part[:2]
                                    field_data = part[2:].strip()
                                    _logger.info(
                                        f"  Field {field_num}: {field_data[:70]}"
                                    )

                                    # If field 22, parse with BankTransactionParser.
                                    if field_num == "22":
                                        parser = BankTransactionParser(
                                            field_data,
                                            bank_swift_id=account_identification[:8],
                                        )
                                        parsed = parser.get_data()
                                        if parsed:
                                            _logger.info(
                                                "    Parsed data from field 22:"
                                            )
                                            for key, value in parsed.items():
                                                _logger.info(f"      {key} {value}")
                                else:
                                    _logger.info(f"  Text: {part[:70]}")

                _logger.info(f"\n{'-'*80}")

            return True

        except UnicodeDecodeError:
            _logger.info(f"✗ Failed with {encoding}")
            continue
        except Exception as e:
            _logger.info(f"✗ Error with {encoding}: {str(e)}")
            continue

    _logger.info("\n✗ Failed to parse file with any encoding")
    return False


def main():
    if len(sys.argv) < 2:
        _logger.info("Usage: python3 test_parser_standalone.py <path_to_mt940_file>")
        _logger.info("\nExample:")
        _logger.info("  python3 test_parser_standalone.py ~/Downloads/statement.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        _logger.info(f"ERROR: File not found: {file_path}")
        sys.exit(1)

    success = parse_mt940_file(file_path)

    if success:
        _logger.info("\n✓ Parsing completed successfully!")
        sys.exit(0)
    else:
        _logger.info("\n✗ Parsing failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
