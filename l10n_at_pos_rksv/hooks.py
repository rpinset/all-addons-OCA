# Copyright 2024 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

# Default mapping between Austrian VAT rates and the RKSV (a.sign)
# tax categories required by the chained signature.
ASIGN_TAX_DEFAULTS = {
    "null": ("0%",),
    "reduced1": ("10%",),
    "reduced2": ("13%",),
    "special": ("19%", "12%"),
}


def post_init_hook(env):
    """Pre-fill ``asign_type`` on the standard Austrian tax groups."""
    tax_group_model = env["account.tax.group"]
    for asign_type, names in ASIGN_TAX_DEFAULTS.items():
        tax_group_model.search(
            [
                ("name", "in", list(names)),
                ("country_id.code", "=", "AT"),
            ]
        ).write({"asign_type": asign_type})
