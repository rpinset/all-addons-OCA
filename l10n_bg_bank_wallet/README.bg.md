# България — Криптиран Crypto Wallet (OCA)

> Per-user криптиран трезор за криптографския материал, нужен на
> банковите + НАП интеграции: RSA ключове, API токени, пароли,
> сертификати. Криптиран at rest, отключван само след автентикация.

**Модул:** `l10n_bg_bank_wallet` | **Версия:** 18.0.1.0.2 | **Лиценз:** LGPL-3 | **Категория:** Localization | **Приложение:** Да

## Описание

Българското банкиране (InfoPay, Borica) и НАП submission flow-овете
изискват частни signing ключове, access токени и пароли.
Съхраняването им в clear-text полета би било критична експозиция.
`l10n_bg_bank_wallet` предоставя модел `crypto.wallet`, в който всяка
тайна е криптирана at rest и декриптируема само от притежаващия
потребител след автентикация — wallet ключът се деривира от
собствения Odoo password hash на потребителя, така че админ, четящ
базата, пак не може да чете чужди ключове.

Стои в самото дъно на графа зависимости (само `base`, `web`).

## Криптография

| Слой | Алгоритъм |
|---|---|
| Деривация на ключ | **PBKDF2-HMAC-SHA256**, 100 000 итерации, per-wallet случаен salt |
| Симетрично криптиране | **Fernet** (AES-256 CBC + HMAC, authenticated) |
| At-rest съхранение | Криптирани blob-ове във filestore — не в БД |
| Обхват на ключа | Деривиран от Odoo password hash → per-user изолация |

Статични помощници в `models/l10n_bg_crypto_wallet.py`:
`generate_salt()`, `derive_key(password, salt)`,
`encrypt_data(data, key)`, `decrypt_data(blob, key)`,
`create_wallet_envelope(...)`.

## Модел на данните

### `crypto.wallet`

- Per-user wallet (`res.users.crypto_wallet_ids` One2many).
- `unlock_wallet_with_password()` / `lock_wallet()` — session-scoped
  отключване; encryption ключът се държи само в session state.
- `add_key_with_user_password(name, type, data)` /
  `get_key_with_user_password(name)` — store/retrieve на тайна.
- `quick_store(...)` / `quick_access(...)` — convenience едноредови.
- `generate_keypair(name, key_type='rsa'|'ec')` — създава
  `<name>_private` + `<name>_public`.
- Disk persistence с filename обфускация.

### `res.users` (разширен — `models/res_users.py`)

При смяна на парола wallet-ите се **автоматично пре-криптират**, така
че смяна на парола никога не orphan-ва съхранените ключове.

## Модел на правата

`security/l10n_bg_crypto_wallet.xml` доставя security групите за
read / write / admin / generate / export; `security/ir.model.access.csv`
ги мапва към ACL-ите на модела.

## Помощници (wizards)

| Wizard | Предназначение |
|---|---|
| `crypto_wallet_add_key_wizard` | добавяне на ключ |
| `crypto_wallet_unlock_wizard` | отключване за сесията |
| `crypto_wallet_change_password_wizard` | пре-криптиране при смяна на парола |
| `crypto_wallet_export_wizard` | експорт на key material |
| `crypto_wallet_key_manager_wizard` | управление на ключове |
| `crypto_wallet_generate_keypair_wizard` | генериране на RSA/EC keypair |

## Употреба

```python
w = env['crypto.wallet'].get_user_wallet_or_create()
w.add_key_with_user_password('infopay_token', 'api_key', 'secret')
val = env['crypto.wallet'].get_user_wallet() \
        .get_key_with_user_password('infopay_token')['data']
env['crypto.wallet'].quick_store('token', 'api_key', 'abc123')
w.generate_keypair('signing', key_type='rsa')
```

## Зависимости

| Odoo базови | Българска локализация | Python пакет |
|---|---|---|
| `base`, `web` | — (фундаментален) | `cryptography` |

## Downstream consumers

`l10n_bg_api_nra` (НАП access token), `l10n_bg_infopay` + EE/OCA
bridges (Borica InfoPay credentials), всеки модул нуждаещ се от
подписани payloads.

## Известни ограничения

- Wallet отключването е session-scoped; дълги idle сесии re-prompt-ват.
- Загуба на Odoo паролата без change-password flow (напр. суров админ
  reset, заобикалящ `res.users` hook) може да заключи съдържанието на
  wallet-а — ползвайте Change Password wizard.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- `readme/DESCRIPTION.md` — изходни бележки
- Consumer: `l10n_bg_api_nra` (token sharing pattern)
