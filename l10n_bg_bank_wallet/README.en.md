# Bulgaria — Encrypted Crypto Wallet (OCA)

> Per-user encrypted vault for the cryptographic material the banking +
> NRA integrations need: RSA keys, API tokens, passwords, certificates.
> Encrypted at rest, unlocked only after authentication.

**Module:** `l10n_bg_bank_wallet` | **Version:** 18.0.1.0.2 | **License:** LGPL-3 | **Category:** Localization | **Application:** Yes

## Overview

Bulgarian banking (InfoPay, Borica) and NRA submission flows require
private signing keys, access tokens and passwords. Storing those in
clear-text fields would be a critical exposure. `l10n_bg_bank_wallet`
provides a `crypto.wallet` model where every secret is encrypted at
rest and only decryptable by the owning user after they authenticate —
the wallet key is derived from the user's own Odoo password hash, so an
admin reading the database still cannot read another user's keys.

It sits at the very bottom of the dependency graph (`base`, `web` only)
so any integration module can rely on it.

## Cryptography

| Layer | Algorithm |
|---|---|
| Key derivation | **PBKDF2-HMAC-SHA256**, 100 000 iterations, per-wallet random salt |
| Symmetric encryption | **Fernet** (AES-256 in CBC + HMAC, authenticated) |
| At-rest storage | Encrypted blobs in the filestore — not in the DB |
| Key scope | Derived from the user's Odoo password hash → per-user isolation |

Static helpers in `models/l10n_bg_crypto_wallet.py`: `generate_salt()`,
`derive_key(password, salt)`, `encrypt_data(data, key)`,
`decrypt_data(blob, key)`, `create_wallet_envelope(...)`.

## Data model

### `crypto.wallet`

- Per-user wallet (`res.users.crypto_wallet_ids` One2many).
- `unlock_wallet_with_password()` / `lock_wallet()` — session-scoped
  unlock; encryption key held only in session state, never persisted.
- `add_key_with_user_password(name, type, data)` /
  `get_key_with_user_password(name)` — store/retrieve a secret.
- `quick_store(name, type, data)` / `quick_access(name)` — convenience
  one-liners used across the localization.
- `generate_keypair(name, key_type='rsa'|'ec')` — creates
  `<name>_private` + `<name>_public` entries in-wallet.
- Disk persistence with filename obfuscation.

### `res.users` (extended — `models/res_users.py`)

On password change, wallets are **automatically re-encrypted** so a
password change never orphans the user's stored keys.

## Permission model

`security/l10n_bg_crypto_wallet.xml` ships the security groups gating
read / write / admin / generate / export operations;
`security/ir.model.access.csv` maps them to the model ACLs.

## Wizards

| Wizard | Purpose |
|---|---|
| `crypto_wallet_add_key_wizard` | add a key |
| `crypto_wallet_unlock_wizard` | unlock the wallet for the session |
| `crypto_wallet_change_password_wizard` | re-encrypt on password change |
| `crypto_wallet_export_wizard` | export key material |
| `crypto_wallet_key_manager_wizard` | manage stored keys |
| `crypto_wallet_generate_keypair_wizard` | generate an RSA/EC keypair |

## Usage

```python
w = env['crypto.wallet'].get_user_wallet_or_create()
w.add_key_with_user_password('infopay_token', 'api_key', 'secret')
val = env['crypto.wallet'].get_user_wallet() \
        .get_key_with_user_password('infopay_token')['data']
env['crypto.wallet'].quick_store('token', 'api_key', 'abc123')
w.generate_keypair('signing', key_type='rsa')
```

## Dependencies

| Odoo core | Bulgarian-localization | External Python |
|---|---|---|
| `base`, `web` | — (foundational) | `cryptography` |

## Downstream consumers

`l10n_bg_api_nra` (NRA access token), `l10n_bg_infopay` + EE/OCA
bridges (Borica InfoPay credentials), any module needing signed
payloads.

## Known limitations

- Wallet unlock is session-scoped; long idle sessions re-prompt.
- Losing the Odoo password without the change-password flow (e.g. a raw
  admin reset bypassing the `res.users` hook) can strand wallet
  contents — use the Change Password wizard.

## See also

- Parent repo overview: [`../OVERVIEW.md`](../OVERVIEW.md)
- `readme/DESCRIPTION.md` — source notes
- Consumer: `l10n_bg_api_nra` (token sharing pattern)
