import os
import tempfile
from zipfile import ZipFile

import requests
from lxml import etree

from odoo import _, models
from odoo.exceptions import UserError


class UpdateBanksWizard(models.TransientModel):
    _name = "update.ru.banks.wizard"
    _description = "Update Banks Russian Wizard"

    _cbr_source_url = "https://cbr.ru/s/newbik"

    def _download_and_extract_cbr_file(self):
        """Download the CBR archive and extract the XML content in
        a temporary directory."""
        try:
            response = requests.get(self._cbr_source_url, timeout=30)
            response.raise_for_status()
        except requests.exceptions.Timeout as e:
            raise UserError(_("Timed out while downloading file from CBR")) from e
        except requests.exceptions.HTTPError as e:
            raise UserError(_("HTTP error while downloading file")) from e
        except requests.exceptions.RequestException as e:
            raise UserError(_("Network error while downloading file: %s") % e) from e

        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "cbr.zip")
            try:
                with open(zip_path, "wb") as f:
                    f.write(response.content)
            except OSError as e:
                raise UserError(_("Failed to save file to disk: %s") % e) from e

            try:
                with ZipFile(zip_path, "r") as zObject:
                    members = zObject.namelist()
                    if not members:
                        raise UserError(_("Downloaded archive is empty"))
                    xml_filename = members[0]
                    zObject.extract(xml_filename, path=temp_dir)
                    xml_path = os.path.join(temp_dir, xml_filename)

                with open(xml_path, "rb") as f:
                    xml_content = f.read()
                return xml_content
            except Exception as e:
                raise UserError(_("Error reading or extracting archive: %s") % e) from e

    def action_import_banks(self):
        xml_content = self._download_and_extract_cbr_file()

        try:
            root = etree.fromstring(xml_content)
        except etree.XMLSyntaxError as e:
            raise UserError(_("Invalid XML format in downloaded file: %s") % e) from e

        bank_model = self.env["res.bank"]
        corracc_model = self.env["res.bank.corracc"]
        country_ru = self.env.ref("base.ru", raise_if_not_found=False)

        count_created = 0
        count_updated = 0

        ns = {"ed": "urn:cbr-ru:ed:v2.0"}

        for entry in root.xpath("//ed:BICDirectoryEntry", namespaces=ns):
            bic = entry.get("BIC")
            if not bic:
                continue

            participant = entry.find("ed:ParticipantInfo", namespaces=ns)
            if participant is None:
                continue

            name = participant.get("NameP", "").strip().upper()
            city = participant.get("Nnp", "").strip()
            street = participant.get("Adr", "").strip()
            zip_code = participant.get("Ind", "").strip()

            bank = bank_model.search([("bic", "=", bic)], limit=1)
            bank_vals = {
                "name": name,
                "bic": bic,
                "city": city,
                "street": street,
                "zip": zip_code,
            }
            if country_ru:
                bank_vals["country"] = country_ru.id

            if bank:
                bank.write(bank_vals)
                count_updated += 1
            else:
                bank = bank_model.create(bank_vals)
                self.env["ir.model.data"].create(
                    {
                        "name": f"res_bank_{bank.id}",
                        "module": "l10n_ru_banks",
                        "model": "res.bank",
                        "res_id": bank.id,
                    }
                )
                count_created += 1

            # Process correspondent accounts
            xml_accounts_map = {}
            for account_elem in entry.findall("ed:Accounts", namespaces=ns):
                acc_number = account_elem.get("Account")
                if acc_number:
                    xml_accounts_map[acc_number] = account_elem

            xml_accounts_set = set(xml_accounts_map.keys())
            odoo_records = bank.corr_acc_ids
            odoo_accounts_map = {r.corr_acc: r for r in odoo_records}
            odoo_accounts_set = set(odoo_accounts_map.keys())

            # Delete obsolete accounts
            to_delete = odoo_accounts_set - xml_accounts_set
            if to_delete:
                records_to_delete = odoo_records.filtered(
                    lambda r, to_delete=to_delete: r.corr_acc in to_delete
                )
                records_to_delete.sudo().unlink()

            # Create new accounts
            to_create = xml_accounts_set - odoo_accounts_set
            for acc in to_create:
                corr = corracc_model.create(
                    {
                        "bank_id": bank.id,
                        "corr_acc": acc,
                    }
                )
                self.env["ir.model.data"].create(
                    {
                        "name": f"res_bank_corracc_{corr.id}",
                        "module": "l10n_ru_banks",
                        "model": "res.bank.corracc",
                        "res_id": corr.id,
                    }
                )

        message = _(
            "Import complete: "
            "%(created_count)s banks created, %(updated_count)s updated."
        ) % {
            count_created,
            count_updated,
        }

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _(
                    "Import of Banks from the Central Bank of the Russian Federation"
                ),
                "message": message,
                "type": "info",
                "sticky": False,
            },
        }
