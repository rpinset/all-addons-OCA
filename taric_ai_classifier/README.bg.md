# България — AI TARIC & INTRASTAT класификатор (OCA)

> Claude-AI автоматична TARIC / INTRASTAT класификация на стокови
> кодове за продукти: описвате продукта, получавате подредени
> предложения с обосновка, прилагате с един клик — единично или batch.

**Модул:** `taric_ai_classifier` | **Версия:** 18.0.1.0.3 | **Лиценз:** LGPL-3 | **Категория:** Accounting/Localizations

> Curated `README.md` (двуезичен, vendor-поддържан) съществува за този
> модул — този файл е developer-handbook придружителят.

## Описание

Задаването на правилния 8-10 цифрен TARIC / CN код на всеки продукт е
досадно и грешкоопасно, но митническите декларации и Intrastat зависят
от него. Този модул изпраща описанието на продукта към **Anthropic
Claude API**, парсва подредените предложения на модела (код + EN/BG
описание + supplementary unit + обосновка + confidence) и позволява на
потребителя да приеме едно — за единичен продукт или цял batch.

## Модел на данните

### `taric.code` (нов — `models/taric_code.py`)

Локалният каталог на TARIC/CN кодове. `_rec_names_search = ["code",
"description"]`, computed `display_name` = `"<код> - <описание>"`.
Методи: `action_view_products()`, `action_verify_code()` (валидира код
срещу външния източник чрез `requests`), плюс AI извикването към
`https://api.anthropic.com/v1/messages`
(`model="claude-sonnet-4-20250514"`).

### `taric.classification.history` (нов)

Одит лог на всяка класификация: продуктът, избраният код, използваният
`ai_model`, timestamp — така че класификационното решение е проследимо.

### `product.template` (разширен — `models/product.py`)

`action_classify_with_ai()` (строи prompt от име + категория +
описание и вика AI), `action_verify_taric_code()`,
`action_view_classification_history()`.

### `res.config.settings` (разширен)

| Настройка | `ir.config_parameter` |
|---|---|
| `anthropic_api_key` | `taric_ai.anthropic_api_key` |
| `auto_classify_enabled` | авто-класификация при create на продукт |
| `auto_apply_high_confidence` | авто-прилагане при висок confidence |

## Помощници (`wizard/`)

| Модел | Роля |
|---|---|
| `taric.classify.wizard` (+ `.suggestion`) | единичен продукт: показва подредени `taric.classify.suggestion` редове (код, description_en/bg, supplementary_unit, reasoning); `action_apply_classification()` записва избрания код + history ред |
| `batch.classify.wizard` (+ `.result`) | много продукти наведнъж: филтър некласифицирани / по категория, опционално авто-прилагане на high-confidence резултати, status feedback |

## Зависимости

| Odoo базови | Българска локализация | Python пакет |
|---|---|---|
| `base`, `product`, `stock`, `stock_delivery`, `account` | — | `requests` |

## Конфигурация

1. Settings → задайте **Anthropic API ключ** (съхранен като
   `ir.config_parameter` `taric_ai.anthropic_api_key`).
2. (Опционално) активирайте авто-класификация при create и
   авто-прилагане за high-confidence резултати.
3. От продукт → **Classify with AI**, или пуснете batch wizard-а върху
   филтриран набор продукти.

## Връзка с `l10n_bg_tariff_code`

`l10n_bg_tariff_code` е митническият rate cache + TARIC/CN полета на
продуктите; този модул е AI front-end-ът, който *попълва* тези кодове.
Ползвайте ги заедно: AI предлага кода, `l10n_bg_tariff_code` резолва
митническата ставка.

## Известни ограничения

- Изисква Anthropic API ключ и изходящ HTTPS; AI предложенията все пак
  трябва да се преглеждат за митнически-критични продукти.
- Качеството на предложенията зависи колко описателни са данните на
  продукта.

## Свързани

- Преглед на репозиторията: [`../OVERVIEW.bg.md`](../OVERVIEW.bg.md)
- Companion: `l10n_bg_tariff_code`
- Curated преглед: `README.md`
