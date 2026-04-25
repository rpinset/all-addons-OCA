# Copyright 2025 Rosen Vladimirov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Bulgarian Banking Integration - Crypto Wallet",
    "version": "18.0.1.0.2",
    "category": "Localization",
    "summary": (
        "Secure storage of cryptographic keys and passwords for banking integrations"
    ),
    "author": "Odoo Community Association (OCA), Rosen Vladimirov",
    "website": "https://github.com/OCA/l10n-bulgaria",
    "license": "LGPL-3",
    "depends": ["base", "web"],
    "data": [
        "security/l10n_bg_crypto_wallet.xml",
        "security/ir.model.access.csv",
        "views/l10n_bg_crypto_wallet.xml",
        "wizards/crypto_wallet_add_key_wizard.xml",
        "wizards/crypto_wallet_unlock_wizard.xml",
        "wizards/crypto_wallet_change_password_wizard.xml",
        "wizards/crypto_wallet_export_wizard.xml",
        "wizards/crypto_wallet_key_manager_wizard.xml",
        "wizards/crypto_wallet_generate_keypair_wizard.xml",
    ],
    "demo": [],
    "images": ["static/description/banner.png"],
    "installable": True,
    "auto_install": False,
    "application": True,
    "external_dependencies": {"python": ["cryptography"]},
    "maintainers": ["rosenvladimirov"],
    "development_status": "Beta",
}
