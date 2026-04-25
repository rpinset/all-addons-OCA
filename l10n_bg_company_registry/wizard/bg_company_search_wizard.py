import logging
import re

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class BgCompanySearchWizard(models.TransientModel):
    """Wizard for searching Bulgarian companies in the registry"""

    _name = "bg.company.search.wizard"
    _description = "Bulgarian Company Search Wizard"

    partner_id = fields.Many2one(
        "res.partner", string="Partner", help="Partner to populate with company data"
    )

    eik = fields.Char(
        string="EIK", help="Company EIK number (9 or 13 digits)", required=True
    )

    original_eik = fields.Char(
        string="Original UIC", help="Original UIC from partner (to detect changes)"
    )

    # Display fields for company data from the registry
    display_eik = fields.Char(string="UIC", readonly=True)
    display_name_bg = fields.Char(string="Company Name (BG)", readonly=True)
    display_name_en = fields.Char(string="Company Name (EN)", readonly=True)
    display_legal_form_bg = fields.Char(string="Legal Form (BG)", readonly=True)
    display_vat = fields.Char(string="VAT Number", readonly=True)
    display_address_bg = fields.Text(string="Address (BG)", readonly=True)
    # Address structured fields
    display_country_id = fields.Many2one("res.country", readonly=True)
    display_state_id = fields.Many2one(
        "res.country.state", string="State", readonly=True
    )
    display_city_id = fields.Many2one("res.city", string="City", readonly=True)
    display_postal_code = fields.Char(string="Postal Code", readonly=True)
    display_street = fields.Char(string="Street", readonly=True)
    display_activity_code = fields.Char(string="Activity Code", readonly=True)
    display_activity_description = fields.Text(
        string="Activity Description", readonly=True
    )
    display_registration_date = fields.Date(string="Registration Date", readonly=True)

    # Store fetched company data as JSON
    company_data_json = fields.Text(
        string="Company Data", readonly=True, help="Raw company data from registry"
    )

    data_fetched = fields.Boolean(
        default=False,
        help="Indicates if data was successfully fetched",
    )

    eik_changed = fields.Boolean(
        string="EIK Changed",
        compute="_compute_eik_changed",
        help="Indicates if EIK was changed by user",
    )

    @api.depends("eik", "original_eik")
    def _compute_eik_changed(self):
        """Check if EIK was changed from the original"""
        for wizard in self:
            wizard.eik_changed = (
                wizard.original_eik and wizard.eik and wizard.eik != wizard.original_eik
            )

    @api.model
    def default_get(self, fields_list):
        """Auto-fetch data when wizard opens if EIK is provided"""
        res = super().default_get(fields_list)

        # If EIK is provided in context, auto-fetch immediately
        if res.get("eik"):
            # Store original EIK
            res["original_eik"] = res["eik"]

            # Try to fetch data automatically
            try:
                eik = self._extract_eik_from_vat(res["eik"])
                if eik:
                    company_data = self._fetch_from_registry_api_eik_only(eik)
                    if company_data:
                        # Resolve relational fields (country, state, city)
                        # Note: We need to use self.env even in default_get
                        # Create a temporary wizard to access self.env
                        temp_wizard = self.env["bg.company.search.wizard"]

                        # Re-parse address to get IDs
                        if company_data.get("address_full_bg"):
                            # Call the instance method via temp_wizard
                            parsed_address = temp_wizard._parse_bulgarian_address(
                                company_data["address_full_bg"]
                            )
                            company_data.update(parsed_address)

                        # Populate display fields
                        res.update(self._populate_display_fields(company_data))
                        res["data_fetched"] = True

                        # Store JSON data
                        import json

                        res["company_data_json"] = json.dumps(
                            company_data, ensure_ascii=False
                        )
            except Exception as e:
                _logger.warning(f"Could not auto-fetch data in wizard: {str(e)}")

        return res

    @staticmethod
    def _extract_eik_from_vat(vat_number):
        """
        Extract EIK from VAT number (removes BG prefix)

        Args:
            vat_number (str): VAT number (can be with or without a BG prefix)

        Returns:
            str: Clean EIK number or False
        """
        if not vat_number:
            return False

        # Remove spaces and convert to uppercase
        vat_clean = vat_number.strip().upper()

        # Remove BG prefix if present
        if vat_clean.startswith("BG"):
            vat_clean = vat_clean[2:]

        # Check if it's a valid EIK (9 or 13 digits)
        if re.match(r"^\d{9}$|^\d{13}$", vat_clean):
            return vat_clean

        return False

    @classmethod
    def _fetch_from_registry_api_eik_only(cls, eik):
        """
        Static method to fetch from registry (without self)
        Used in default_get
        """
        if not eik:
            return False

        try:
            _logger.info(
                "Fetching company data from portal.registryagency.bg API for "
                "EIK: %s",
                eik,
            )

            api_url = f"https://portal.registryagency.bg/CR/api/Deeds/{eik}"

            from datetime import datetime

            current_date = datetime.now().strftime("%Y-%m-%dT23:59:59.999Z")

            response = requests.get(
                api_url,
                params={
                    "entryDate": current_date,
                    "loadFieldsFromAllLegalForms": "false",
                },
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; Odoo/18.0)",
                    "Accept": "*/*",
                    "Content-Type": "application/json; charset=utf-8",
                },
                timeout=30,
            )

            if response.status_code == 200:
                _logger.info(f"Successfully fetched company data for EIK: {eik}")
                data = response.json()
                return cls._parse_registry_response_static(data)
            else:
                _logger.warning(
                    "Registry API returned status %s for EIK: %s",
                    response.status_code,
                    eik,
                )
                return False

        except Exception as e:
            _logger.error(f"Error fetching from registry: {str(e)}")
            return False

    def _parse_bulgarian_address(self, address_text):
        """
        Instance method wrapper for address parsing
        Also resolves city_id and state_id from a database
        """
        result = self._parse_bulgarian_address_static(address_text)

        # Force Bulgarian language context for all searches
        # since registry data is only in Bulgarian
        bg_env = self.env(context=dict(self.env.context, lang="bg_BG"))

        # Resolve country_id
        if result.get("country_name"):
            # Try to find a country by name (e.g., "БЪЛГАРИЯ")
            # Using =ilike for exact case-insensitive match
            country = bg_env["res.country"].search(
                [("name", "=ilike", result["country_name"])], limit=1
            )

            # If not found by name, try by code
            if not country and result.get("country_code"):
                country = bg_env["res.country"].search(
                    [("code", "=", result["country_code"])], limit=1
                )

            if country:
                result["country_id"] = country.id
                # Remove country_name as we have country_id now
                del result["country_name"]

        # Resolve state_id
        if result.get("state_name"):
            state = False

            # Първо опитваме точно съвпадение
            state = bg_env["res.country.state"].search(
                [
                    ("country_id.code", "=", "BG"),
                    ("name", "ilike", result["state_name"]),
                ],
                limit=1,
            )

            # Ако не е намерена, добавяме префикс
            # "Област " и търсим отново
            if not state:
                state_name_with_prefix = f"Област {result['state_name']}"
                state = bg_env["res.country.state"].search(
                    [
                        ("country_id.code", "=", "BG"),
                        ("name", "ilike", state_name_with_prefix),
                    ],
                    limit=1,
                )

            if state:
                result["state_id"] = state.id

        # Resolve city_id
        if result.get("city_name"):
            city = False
            # Опитваме се първо по пощенски код
            if result.get("zip"):
                city = bg_env["res.city"].search(
                    [("country_id.code", "=", "BG"), ("zipcode", "=", result["zip"])]
                )

                # Ако има повече от един град с този
                # пощенски код, филтрираме по име
                if len(city) > 1:
                    # Case-insensitive exact match
                    city = city.filtered(
                        lambda c: c.name.lower() == result["city_name"].lower()
                    )
                    if not city:
                        # Опитваме се с частично съвпадение
                        # (ilike за pattern matching)
                        city = bg_env["res.city"].search(
                            [
                                ("country_id.code", "=", "BG"),
                                ("zipcode", "=", result["zip"]),
                                ("name", "ilike", result["city_name"]),
                            ],
                            limit=1,
                        )

            # Ако не е намерен по пощенски код,
            # опитваме се по име
            if not city:
                # Using =ilike for exact case-insensitive match
                city = bg_env["res.city"].search(
                    [
                        ("country_id.code", "=", "BG"),
                        ("name", "=ilike", result["city_name"]),
                    ],
                    limit=1,
                )

            if city:
                result["city_id"] = city.id

        return result

    @staticmethod
    def _parse_bulgarian_address_static(address_text):
        """
        Parse Bulgarian address and map to city_id
        Static version for use in default_get

        Args:
            address_text (str): Full address text from registry

        Returns:
            dict: Parsed address components with city_id
        """
        if not address_text:
            return {}

        result = BgCompanySearchWizard._init_address_result()

        # Split the address by newlines to process each line
        lines = [line.strip() for line in address_text.split("\n") if line.strip()]

        for line in lines:
            if BgCompanySearchWizard._parse_country_line(line, result):
                continue
            if BgCompanySearchWizard._parse_state_line(line, result):
                continue
            if BgCompanySearchWizard._parse_city_line(line, result):
                continue
            if BgCompanySearchWizard._parse_district_line(line, result):
                continue
            if BgCompanySearchWizard._parse_email_line(line, result):
                continue
            if BgCompanySearchWizard._parse_street_line(line, result):
                continue

        return result

    @staticmethod
    def _init_address_result():
        return {
            "country_code": "BG",
            "country_name": "",
            "state_id": False,
            "state_name": "",
            "city_id": False,
            "city_name": "",
            "zip": "",
            "district": "",
            "street": "",
            "street_name": "",
            "street_number": "",
            "street_number2": "",
            "street_building_number": "",
            "street_floor_number": "",
            "phone": "",
            "email": "",
        }

    @staticmethod
    def _parse_country_line(line, result):
        if not line.startswith("Държава:"):
            return False
        country_match = re.search(r"Държава:\s*(.+)$", line)
        if country_match:
            result["country_name"] = country_match.group(1).strip()
        return True

    @staticmethod
    def _parse_state_line(line, result):
        if "Област:" not in line:
            return False
        # Format: "Област: Разград, Община: Разград"
        state_match = re.search(r"Област:\s*([^,]+)", line)
        if state_match:
            result["state_name"] = state_match.group(1).strip()
        return True

    @staticmethod
    def _parse_city_line(line, result):
        if "Населено място:" not in line:
            return False
        city_match = re.search(
            r"Населено място:\s*(?:гр\.|с\.)\s*([^,]+?)" r"(?:,\s*п\.к\.\s*(\d+))?$",
            line,
        )
        if city_match:
            result["city_name"] = city_match.group(1).strip()
            if city_match.group(2):
                result["zip"] = city_match.group(2).strip()
        return True

    @staticmethod
    def _parse_district_line(line, result):
        if not line.startswith("р-н"):
            return False
        district_match = re.search(r"р-н\s+(.+)$", line)
        if district_match:
            result["district"] = district_match.group(1).strip()
        return True

    @staticmethod
    def _parse_email_line(line, result):
        if "Адрес на електронна поща:" not in line:
            return False
        email_pattern = r"Адрес на електронна поща:\s*(.+)$"
        email_match = re.search(email_pattern, line)
        if email_match:
            result["email"] = email_match.group(1).strip()
        return True

    @staticmethod
    def _parse_street_line(line, result):
        if "бул./ул." not in line:
            return False
        # Формат: "ж.к. Младост 4, бул./ул. Самара № 2,
        # бл. Адванс Бизнес Център, сграда 2, ет. 8"
        street_match = re.search(r"бул\./ул\.\s*(.+)$", line)
        if not street_match:
            return True

        full_street_line = street_match.group(1).strip()
        street_line = BgCompanySearchWizard._strip_contact_from_street_line(
            full_street_line,
            result,
        )
        street_line = re.sub(r"^(?:бул\.|ул\.)\.?\s*", "", street_line)
        street_line = street_line.replace('"', "")

        segments = [seg.strip() for seg in street_line.split(",")]
        components = BgCompanySearchWizard._parse_street_segments(segments)

        BgCompanySearchWizard._apply_street_components(result, components)
        result["street"] = BgCompanySearchWizard._build_full_street(
            result,
            components,
            line,
        )
        return True

    @staticmethod
    def _strip_contact_from_street_line(full_street_line, result):
        contact_pattern = r"\s+(?:Телефон|Факс):\s*(.+)$"
        contact_match = re.search(contact_pattern, full_street_line)
        if not contact_match:
            return full_street_line
        contact_info = contact_match.group(1).strip()
        if "@" in contact_info:
            result["email"] = contact_info
        else:
            result["phone"] = contact_info
        return re.sub(r"\s+(?:Телефон|Факс):.+$", "", full_street_line)

    @staticmethod
    def _parse_street_segments(segments):
        components = {
            "street_name": "",
            "street_number": "",
            "building_number": "",
            "building_name": "",
            "entrance": "",
            "floor_number": "",
            "apartment": "",
        }
        for segment in segments:
            if "№" in segment and not components["street_number"]:
                parts = segment.split("№")
                if parts[0].strip() and not components["street_name"]:
                    components["street_name"] = parts[0].strip()
                if len(parts) > 1:
                    num_match = re.search(r"(\d+[А-Яа-я]?)", parts[1])
                    if num_match:
                        components["street_number"] = num_match.group(1)
                continue

            if segment.startswith("бл."):
                building_text = segment[3:].strip()
                if re.match(r"^\d+[А-Яа-я]?$", building_text):
                    components["building_number"] = building_text
                else:
                    components["building_name"] = building_text
                continue

            if segment.startswith("вх."):
                components["entrance"] = segment[3:].strip()
                continue

            if segment.startswith("ет."):
                floor_match = re.search(r"(\d+)", segment)
                if floor_match:
                    components["floor_number"] = floor_match.group(1)
                continue

            if segment.startswith("ап."):
                apt_match = re.search(r"(\d+)", segment)
                if apt_match:
                    components["apartment"] = apt_match.group(1)
                continue

            if segment.startswith("сграда"):
                if components["building_name"]:
                    components["building_name"] += f", {segment}"
                else:
                    components["building_name"] = segment
                continue

            if not components["street_name"] and not any(
                keyword in segment for keyword in ["бл.", "вх.", "ет.", "ап.", "сграда"]
            ):
                components["street_name"] = segment

        return components

    @staticmethod
    def _apply_street_components(result, components):
        if components["street_name"]:
            result["street_name"] = components["street_name"]
        if components["street_number"]:
            result["street_number"] = components["street_number"]
        if components["apartment"]:
            result["street_number2"] = components["apartment"]

        building_parts = []
        if components["building_number"]:
            building_parts.append(components["building_number"])
        if components["building_name"]:
            building_parts.append(components["building_name"])
        if components["entrance"]:
            building_parts.append(f"вх. {components['entrance']}")

        if building_parts:
            result["street_building_number"] = ", ".join(building_parts)
        elif components["entrance"]:
            result["street_building_number"] = f"вх. {components['entrance']}"

        if components["floor_number"]:
            result["street_floor_number"] = components["floor_number"]

    @staticmethod
    def _build_full_street(result, components, line):
        street_parts = []
        if result.get("district"):
            street_parts.append(f"р-н {result['district']}")
        if "ж.к." in line:
            complex_match = re.search(r"ж\.к\.\s*([^,]+)", line)
            if complex_match:
                street_parts.append(f"ж.к. {complex_match.group(1).strip()}")
        if components["street_name"]:
            street_parts.append(components["street_name"])
        if components["street_number"]:
            street_parts.append(f"№ {components['street_number']}")
        if components["building_number"]:
            street_parts.append(f"бл. {components['building_number']}")
        if components["building_name"]:
            street_parts.append(components["building_name"])
        if components["entrance"]:
            street_parts.append(f"вх. {components['entrance']}")
        if components["floor_number"]:
            street_parts.append(f"ет. {components['floor_number']}")
        if components["apartment"]:
            street_parts.append(f"ап. {components['apartment']}")
        return ", ".join(street_parts)

    @staticmethod
    def _format_company_name(name):
        """
        Format company name to Title Case

        Args:
            name (str): Company name in uppercase

        Returns:
            str: Formatted company name
        """
        if not name:
            return name

        # Разделяме по интервали и форматираме
        # всяка дума
        words = name.split()
        formatted_words = []

        for word in words:
            # Запазваме съкращенията с главни букви
            # (2-3 букви)
            if len(word) <= 3 and word.isupper():
                formatted_words.append(word)
            else:
                # Title case за останалите думи
                formatted_words.append(word.capitalize())

        return " ".join(formatted_words)

    @staticmethod
    def _format_person_name(name):
        """
        Format person name: First and middle names in Title Case, last name in UPPERCASE

        Args:
            name (str): Person name (usually 3 parts: first middle last)

        Returns:
            str: Formatted person name
        """
        if not name:
            return name

        # Разделяме имената
        name_parts = name.split()

        if len(name_parts) == 0:
            return name
        elif len(name_parts) == 1:
            # Само едно име - правим го Title Case
            return name_parts[0].capitalize()
        elif len(name_parts) == 2:
            # Две имена - първото Title Case, второто UPPERCASE
            return f"{name_parts[0].capitalize()} {name_parts[1].upper()}"
        else:
            # Три или повече имена - последното UPPERCASE,
            # останалите Title Case
            formatted_parts = [part.capitalize() for part in name_parts[:-1]]
            formatted_parts.append(name_parts[-1].upper())
            return " ".join(formatted_parts)

    @staticmethod
    def _get_legal_form_bg(legal_form_code):
        legal_forms = {
            10: "ЕООД",
            4: "ООД",
            5: "АД",
            11: "ЕАД",
            3: "КД",
            6: "КДА",
            2: "СД",
            1: "ЕТ",
        }
        return legal_forms.get(legal_form_code, "")

    @staticmethod
    def _build_company_name_bg(company_name_bg_raw, legal_form_bg):
        company_name_bg = BgCompanySearchWizard._format_company_name(
            company_name_bg_raw
        )
        if legal_form_bg:
            return company_name_bg, f"{company_name_bg} {legal_form_bg}"
        return company_name_bg, company_name_bg

    @staticmethod
    def _extract_company_name_en(sections):
        for section in sections:
            for sub_deed in section.get("subDeeds", []):
                for group in sub_deed.get("groups", []):
                    for field in group.get("fields", []):
                        if field.get("nameCode") == "CR_F_4_L":
                            html_data = field.get("htmlData", "")
                            text = re.sub(r"<[^>]+>", "", html_data)
                            return " ".join(text.split()).strip()
        return ""

    @staticmethod
    def _build_company_name_en(company_name_en_raw, company_name_bg, legal_form_bg):
        if company_name_en_raw:
            company_name_en_raw = BgCompanySearchWizard._format_company_name(
                company_name_en_raw
            )

        legal_form_en_map = {
            "ЕООД": "Ltd.",
            "ООД": "Ltd.",
            "АД": "JSC",
            "ЕАД": "JSC",
            "КД": "LP",
            "КДА": "PLS",
            "СД": "GP",
            "ЕТ": "ET",
        }
        legal_form_en = legal_form_en_map.get(legal_form_bg, "")

        if company_name_en_raw and legal_form_en:
            return f"{company_name_en_raw} {legal_form_en}"
        if company_name_en_raw:
            return company_name_en_raw
        if company_name_bg and legal_form_en:
            return f"{company_name_bg} {legal_form_en}"
        return company_name_bg

    @staticmethod
    def _build_company_data_base(
        data,
        company_name_bg_full,
        company_name_en,
        legal_form_bg,
    ):
        return {
            "eik": data.get("uic", ""),
            "company_name_bg": company_name_bg_full,
            "company_name_en": company_name_en,
            "legal_form_bg": legal_form_bg,
            "vat_number": f"BG{data.get('uic', '')}" if data.get("uic") else "",
            "status": "active",
            "managers": [],
        }

    @staticmethod
    def _parse_sections_into_company_data(company_data, sections):
        handlers = {
            "CR_F_5_L": BgCompanySearchWizard._handle_address_field,
            "CR_F_6_L": BgCompanySearchWizard._handle_activity_field,
            "CR_F_6a_L": BgCompanySearchWizard._handle_activity_code_field,
            "CR_F_7_L": BgCompanySearchWizard._handle_managers_field,
            "CR_F_1_L": BgCompanySearchWizard._handle_registration_date_field,
        }
        for section in sections:
            for sub_deed in section.get("subDeeds", []):
                for group in sub_deed.get("groups", []):
                    for field in group.get("fields", []):
                        field_code = field.get("nameCode", "")
                        handler = handlers.get(field_code)
                        if handler:
                            handler(company_data, field)

    @staticmethod
    def _handle_address_field(company_data, field):
        html_data = field.get("htmlData", "")
        text = re.sub(r"<br\s*/?>", "\n", html_data)
        text = re.sub(r"<[^>]+>", "", text)
        lines = [" ".join(line.split()) for line in text.split("\n")]
        text = "\n".join(lines).strip()
        company_data["address_full_bg"] = text

        parsed_address = BgCompanySearchWizard._parse_bulgarian_address_static(text)
        company_data.update(parsed_address)

    @staticmethod
    def _handle_activity_field(company_data, field):
        html_data = field.get("htmlData", "")
        text = re.sub(r"<[^>]+>", "", html_data)
        company_data["activity_description_bg"] = " ".join(text.split()).strip()

    @staticmethod
    def _handle_activity_code_field(company_data, field):
        html_data = field.get("htmlData", "")
        text = re.sub(r"<[^>]+>", "", html_data)
        match = re.search(r"Група по НКИД:\s*(\d+)", text)
        if match:
            company_data["activity_code"] = match.group(1).strip()

    @staticmethod
    def _handle_managers_field(company_data, field):
        html_data = field.get("htmlData", "")
        text = re.sub(r"<[^>]+>", "", html_data)
        text = " ".join(text.split()).strip()

        manager_entries = text.split(",")
        for manager_entry in manager_entries:
            manager_data = BgCompanySearchWizard._parse_manager_entry(manager_entry)
            if manager_data:
                company_data["managers"].append(manager_data)

    @staticmethod
    def _parse_manager_entry(manager_entry):
        manager_entry = manager_entry.strip()
        if not manager_entry:
            return None

        manager_data = {}
        country_match = re.search(r"Държава:\s*([^\n,]+)", manager_entry)
        if country_match:
            manager_data["country"] = country_match.group(1).strip()
            name_part = manager_entry.split("Държава:")[0].strip()
        else:
            name_part = manager_entry.strip()

        if not name_part:
            return None

        manager_data["name"] = BgCompanySearchWizard._format_person_name(name_part)
        return manager_data

    @staticmethod
    def _handle_registration_date_field(company_data, field):
        action_date = field.get("fieldActionDate", "")
        if action_date:
            company_data["registration_date"] = action_date.split("T")[0]

    @staticmethod
    def _parse_registry_response_static(data):
        """Static parser for registry response"""
        try:
            legal_form_bg = BgCompanySearchWizard._get_legal_form_bg(
                data.get("legalForm")
            )
            company_name_bg, company_name_bg_full = (
                BgCompanySearchWizard._build_company_name_bg(
                    data.get("companyName", ""),
                    legal_form_bg,
                )
            )
            company_name_en_raw = BgCompanySearchWizard._extract_company_name_en(
                data.get("sections", [])
            )
            company_name_en = BgCompanySearchWizard._build_company_name_en(
                company_name_en_raw,
                company_name_bg,
                legal_form_bg,
            )

            company_data = BgCompanySearchWizard._build_company_data_base(
                data,
                company_name_bg_full,
                company_name_en,
                legal_form_bg,
            )

            BgCompanySearchWizard._parse_sections_into_company_data(
                company_data,
                data.get("sections", []),
            )

            return company_data

        except Exception as e:
            _logger.error(f"Error parsing registry response: {str(e)}")
            return False

    @staticmethod
    def _populate_display_fields(company_data):
        """Populate display fields from company data"""
        return {
            "display_eik": company_data.get("eik", ""),
            "display_name_bg": company_data.get("company_name_bg", ""),
            "display_name_en": company_data.get("company_name_en", ""),
            "display_legal_form_bg": company_data.get("legal_form_bg", ""),
            "display_vat": company_data.get("vat_number", ""),
            "display_address_bg": company_data.get("address_full_bg", ""),
            "display_country_id": company_data.get("country_id", False),
            "display_state_id": company_data.get("state_id", False),
            "display_city_id": company_data.get("city_id", False),
            "display_postal_code": company_data.get("zip", ""),
            "display_street": company_data.get("street", ""),
            "display_activity_code": company_data.get("activity_code", ""),
            "display_activity_description": company_data.get(
                "activity_description_bg", ""
            ),
            "display_registration_date": company_data.get("registration_date", False),
        }

    def _fetch_from_registry_api(self, eik):
        """Instance method wrapper"""
        return self._fetch_from_registry_api_eik_only(eik)

    def _parse_registry_api_response(self, data):
        """Instance method wrapper"""
        return self._parse_registry_response_static(data)

    @staticmethod
    def _extract_nkid_code(html_data):
        """Extract NKID code from HTML"""
        text = re.sub(r"<[^>]+>", "", html_data)
        text = " ".join(text.split()).strip()
        match = re.search(r"Група по НКИД:\s*(\d+)", text)
        if match:
            return match.group(1).strip()
        return ""

    def action_populate_partner(self):
        """Populate partner with fetched company data"""
        self.ensure_one()

        if not self.data_fetched:
            raise UserError(_("Моля първо изтеглете данните от " "регистъра"))

        if not self.partner_id:
            raise UserError(_("Няма зададен партньор"))

        # Get company data from JSON
        import json

        # Проверка дали има валиден JSON
        if not self.company_data_json:
            raise UserError(
                _('No registry data saved. Please press "Download Data" again.')
            )

        try:
            company_data = json.loads(self.company_data_json)
        except (json.JSONDecodeError, TypeError) as e:
            raise UserError(_("Error reading data from registry: %s") % str(e)) from e

        # Reparse address to get city_id and state_id
        if company_data.get("address_full_bg"):
            parsed_address = self._parse_bulgarian_address(
                company_data["address_full_bg"]
            )
            company_data.update(parsed_address)

        # Prepare partner values
        vals = self._prepare_partner_vals_from_company_data(company_data)

        # Update partner
        self.partner_id.write(vals)
        self.partner_id.update_field_translations(
            "name",
            {
                "en_US": self.display_name_en,
            },
        )

        # Create or update a representative contact
        if company_data.get("managers") and len(company_data["managers"]) > 0:
            # Вземаме първия управител
            manager = company_data["managers"][0]

            # Търсим съществуващ представител
            existing_represent = self.partner_id.child_ids.filtered(
                lambda r: r.type == "represent"
            )

            manager_vals = {
                "name": manager.get("name", ""),
                "type": "represent",
                "parent_id": self.partner_id.id,
            }

            # Добавяме държава ако е налична
            # (search with bg_BG context)
            if manager.get("country"):
                bg_env = self.env(context=dict(self.env.context, lang="bg_BG"))
                # Using =ilike for exact case-insensitive match
                country = bg_env["res.country"].search(
                    [("name", "=ilike", manager["country"])], limit=1
                )
                if country:
                    manager_vals["country_id"] = country.id

            if existing_represent:
                # Актуализираме съществуващия
                existing_represent.write(manager_vals)
            else:
                # Създаваме нов
                self.env["res.partner"].create(manager_vals)

        return {"type": "ir.actions.act_window_close"}

    def action_fetch_data(self):
        """Fetch company data from a registry (manual refresh)"""
        self.ensure_one()

        if not self.eik:
            raise ValidationError(_("Please enter the UIC number"))

        # Extract EIK from VAT if needed
        eik = self._extract_eik_from_vat(self.eik)

        if not eik:
            raise ValidationError(_("Invalid UIC format. Please enter 9 or 13 digits."))

        # Fetch from registry API
        company_data = self._fetch_from_registry_api(eik)

        if not company_data:
            raise UserError(
                _(
                    "No company with UIC was found: %s\n\n"
                    "The company was not found in the official trade register.\n\n"
                    "Please check if the UIC number is correct."
                )
                % eik
            )

        # Re-parse address to get city_id, state_id, country_id
        if company_data.get("address_full_bg"):
            parsed_address = self._parse_bulgarian_address(
                company_data["address_full_bg"]
            )
            company_data.update(parsed_address)

        # Store data in JSON format
        import json

        self.company_data_json = json.dumps(company_data, ensure_ascii=False)
        self.data_fetched = True

        # Update original EIK
        self.original_eik = self.eik

        # Populate display fields
        display_vals = self._populate_display_fields(company_data)
        self.write(display_vals)

        return {
            "type": "ir.actions.act_window",
            "res_model": "bg.company.search.wizard",
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
            "context": self.env.context,
        }

    @api.model
    def _prepare_partner_vals_from_company_data(self, company_data):
        """
        Prepare partner values from company data

        Args:
            company_data (dict): Company data from a registry

        Returns:
            dict: Partner values
        """
        vals = {}

        def set_if(src_key, dest_key):
            value = company_data.get(src_key)
            if value:
                vals[dest_key] = value

        set_if("company_name_bg", "name")

        eik = company_data.get("eik")
        if eik:
            vals["l10n_bg_uic"] = eik
            vals["l10n_bg_uic_type"] = "bg_uic"

        set_if("vat_number", "vat")
        set_if("legal_form_bg", "l10n_bg_legal_form")
        set_if("city_id", "city_id")
        set_if("state_id", "state_id")
        set_if("zip", "zip")
        set_if("street_name", "street_name")
        set_if("street_number", "street_number")
        set_if("street_number2", "street_number2")

        partner_fields = self.env["res.partner"]._fields
        optional_fields = [
            "street_building_number",
            "street_floor_number",
            "street_sector_number",
        ]
        for field_name in optional_fields:
            if field_name in partner_fields and company_data.get(field_name):
                vals[field_name] = company_data[field_name]

        if company_data.get("street"):
            vals["street"] = company_data["street"]

        # Phone and Email
        if company_data.get("phone"):
            vals["phone"] = company_data["phone"]

        if company_data.get("email"):
            vals["email"] = company_data["email"]

        # Country - use country_id if available, otherwise default to BG
        if company_data.get("country_id"):
            vals["country_id"] = company_data["country_id"]
        else:
            # Fallback to Bulgaria
            country_bg = self.env["res.country"].search([("code", "=", "BG")], limit=1)
            if country_bg:
                vals["country_id"] = country_bg.id

        # Registration date
        if company_data.get("registration_date"):
            vals["l10n_bg_registration_date"] = company_data["registration_date"]

        # Activity
        if company_data.get("activity_code"):
            vals["l10n_bg_activity_code"] = company_data["activity_code"]

        if company_data.get("activity_description_bg"):
            vals["l10n_bg_activity_description"] = company_data[
                "activity_description_bg"
            ]

        # Set as a company
        vals["is_company"] = True
        vals["company_type"] = "company"

        return vals
