import {barcodeParsers} from "@barcode_scanner/js/registries.esm";
import {
    compileGs1Rule,
    getGs1Nomenclature,
    hasValidCheckDigit,
} from "@barcode_gs1/js/gs1_nomenclature.esm";

const GS1_SEPARATOR = String.fromCharCode(29); // FNC1 (<GS>, 0x1D)

// The symbology identifiers the GS1 carriers prefix their data with: GS1-128,
// DataBar, GS1 DataMatrix, GS1 QR and GS1 DotCode. Their presence is itself
// proof that what follows is GS1 data ("]E0", a plain EAN-13, is not one of
// them).
const GS1_SYMBOLOGIES = ["]C1", "]e0", "]d2", "]Q3", "]J1"];

// An application identifier written in parentheses, as on the human-readable
// line of a label: "(01)", "(3103)".
const PARENTHESISED_AI = /\(\d{2,4}\)/;

// Logistic measures (AI 330n-349n: the gross weight, dimensions and volume of
// the logistic unit) describe the pack, not the goods it holds.
const LOGISTIC_MEASURE_AI = /^3[34]/;

// The characters GS1 allows in an alphanumeric value, as Odoo's own rules
// spell them out.
const ALPHA = '[!"%-/0-9:-?A-Z_a-z]';

/**
 * Built-in application identifiers, written as `barcode.rule` patterns so they
 * compile exactly like the ones read from the nomenclature.
 *
 * They are the fallback: the parser prefers the configured GS1 nomenclature and
 * only reaches for these while it is still loading, when no GS1 nomenclature is
 * configured, or for an identifier the nomenclature does not define (Odoo ships
 * no rule for a production date, for instance) — otherwise an unknown AI in the
 * middle of a barcode would cut the rest of the scan short.
 */
const BUILTIN_RULE_DEFS = [
    {
        name: "SSCC",
        pattern: "(00)(\\d{18})",
        type: "package",
        gs1_content_type: "identifier",
    },
    {
        name: "GTIN",
        pattern: "(01)(\\d{14})",
        type: "product",
        gs1_content_type: "identifier",
    },
    {
        name: "GTIN of contained trade items",
        pattern: "(02)(\\d{14})",
        type: "product",
        gs1_content_type: "identifier",
    },
    {
        name: "Batch or lot number",
        pattern: `(10)(${ALPHA}{0,20})`,
        type: "lot",
        gs1_content_type: "alpha",
    },
    {
        name: "Production date",
        pattern: "(11)(\\d{6})",
        type: "production_date",
        gs1_content_type: "date",
    },
    {
        name: "Pack date",
        pattern: "(13)(\\d{6})",
        type: "pack_date",
        gs1_content_type: "date",
    },
    {
        name: "Best before date",
        pattern: "(15)(\\d{6})",
        type: "use_date",
        gs1_content_type: "date",
    },
    {
        name: "Sell by date",
        pattern: "(16)(\\d{6})",
        type: "use_date",
        gs1_content_type: "date",
    },
    {
        name: "Expiration date",
        pattern: "(17)(\\d{6})",
        type: "expiration_date",
        gs1_content_type: "date",
    },
    {
        name: "Product variant",
        pattern: "(20)(\\d{2})",
        type: null,
        gs1_content_type: "alpha",
    },
    {
        name: "Serial number",
        pattern: `(21)(${ALPHA}{0,20})`,
        type: "lot",
        gs1_content_type: "alpha",
    },
    {
        name: "Consumer product variant",
        pattern: `(22)(${ALPHA}{0,20})`,
        type: null,
        gs1_content_type: "alpha",
    },
    {
        name: "Variable count of items",
        pattern: "(30)(\\d{0,8})",
        type: "quantity",
        gs1_content_type: "measure",
        gs1_decimal_usage: false,
    },
    {
        name: "Measure (weight, length, volume, ...)",
        pattern: "(3[1-6]\\d[0-5])(\\d{6})",
        type: "quantity",
        gs1_content_type: "measure",
        gs1_decimal_usage: true,
        generic: true,
    },
    {
        name: "Count of trade items",
        pattern: "(37)(\\d{0,8})",
        type: "quantity",
        gs1_content_type: "measure",
        gs1_decimal_usage: false,
    },
    {
        name: "Amount payable, single monetary area",
        pattern: "(39[02][0-9])(\\d{0,15})",
        type: "price",
        gs1_content_type: "measure",
        gs1_decimal_usage: true,
    },
    {
        // The value opens with the 3-digit ISO 4217 code of its currency.
        name: "Amount payable with ISO currency code",
        pattern: "(39[13][0-9])(\\d{3,18})",
        type: "price",
        gs1_content_type: "measure",
        gs1_decimal_usage: true,
    },
    {
        name: "Ship to / Deliver to GLN",
        pattern: "(410)(\\d{13})",
        type: "location_dest",
        gs1_content_type: "identifier",
    },
    {
        name: "Ship for / Deliver for GLN",
        pattern: "(413)(\\d{13})",
        type: "location_dest",
        gs1_content_type: "identifier",
    },
    {
        name: "Physical location GLN",
        pattern: "(414)(\\d{13})",
        type: "location",
        gs1_content_type: "identifier",
    },
    {
        name: "Package type",
        pattern: `(91)(${ALPHA}{0,90})`,
        type: "package_type",
        gs1_content_type: "alpha",
    },
    {
        name: "Company internal information",
        pattern: `(9[0-3])(${ALPHA}{0,30})`,
        type: null,
        gs1_content_type: "alpha",
        generic: true,
    },
];

const BUILTIN_RULES = BUILTIN_RULE_DEFS.map(compileGs1Rule).filter(Boolean);

/**
 * The rules to parse with: the configured GS1 nomenclature first — so an
 * administrator's rule always wins — then the built-in identifiers.
 */
function activeRules() {
    const nomenclature = getGs1Nomenclature();
    return nomenclature ? [...nomenclature.rules, ...BUILTIN_RULES] : BUILTIN_RULES;
}

/**
 * The year a 2-digit GS1 year refers to, per section 7.12 of the GS1 General
 * Specifications: the closest year within -49/+50 of the current one.
 */
function gs1Year(twoDigitYear) {
    const now = new Date();
    const difference = twoDigitYear - (now.getFullYear() % 100);
    let century = Math.floor(now.getFullYear() / 100);
    if (difference >= 51 && difference <= 99) {
        century -= 1;
    } else if (difference >= -99 && difference <= -50) {
        century += 1;
    }
    return century * 100 + twoDigitYear;
}

function toISODate(value) {
    if (!/^\d{6}$/.test(value)) {
        return null;
    }
    const year = gs1Year(parseInt(value.slice(0, 2), 10));
    const month = parseInt(value.slice(2, 4), 10);
    let day = parseInt(value.slice(4, 6), 10);
    if (month < 1 || month > 12) {
        return null;
    }
    if (day === 0) {
        // GS1 allows DD = 00, meaning the last day of the month.
        day = new Date(Date.UTC(year, month, 0)).getUTCDate();
    }
    const candidate = new Date(Date.UTC(year, month - 1, day));
    if (
        candidate.getUTCFullYear() !== year ||
        candidate.getUTCMonth() !== month - 1 ||
        candidate.getUTCDate() !== day
    ) {
        return null;
    }
    return `${year.toString().padStart(4, "0")}-${month
        .toString()
        .padStart(2, "0")}-${day.toString().padStart(2, "0")}`;
}

/**
 * Every form of a GTIN that a product barcode may hold, in priority order.
 *
 * GS1 always carries the GTIN zero-padded to 14 digits, while products store
 * the short code printed on the item (EAN13, UPC-A, EAN8). Stripping the
 * padding is therefore part of reading a GS1 scan, not of matching a product.
 */
export function gtinVariants(gtin) {
    const digits = String(gtin || "").replace(/\D/g, "");
    if (!digits) {
        return [];
    }
    const significant = digits.replace(/^0+/, "") || "0";
    const variants = [];
    // 13 first: Odoo's `sanitize_ean` stores barcodes as EAN13, so a UPC-A is
    // held as a 13-digit code too. The other lengths cover codes stored raw.
    for (const length of [13, 14, 12, 8]) {
        if (significant.length <= length) {
            variants.push(significant.padStart(length, "0"));
        }
    }
    variants.push(digits, significant);
    return [...new Set(variants)];
}

/**
 * The GTIN form to match a product against: the EAN13-length code when the GTIN
 * fits in one, otherwise the 14-digit code as scanned (a genuine ITF-14).
 */
export function gtinToProductCode(gtin) {
    return gtinVariants(gtin)[0] || null;
}

function normalizeBarcode(barcode) {
    let value = String(barcode || "").trim();
    // Strip a leading symbology identifier such as "]C1" / "]d2".
    if (/^\][A-Za-z0-9]{2}/.test(value)) {
        value = value.slice(3);
    }
    if (value.startsWith(GS1_SEPARATOR)) {
        value = value.slice(1);
    }
    return value;
}

/**
 * The nomenclature may declare its own separator characters, since a scanner
 * that cannot emit FNC1 often sends "#" instead. This runs once the barcode is
 * known to be GS1, never before: a product code that happens to contain such a
 * character must not start looking like GS1 data because of it.
 */
function applyAlternativeSeparators(barcode) {
    const separator = getGs1Nomenclature()?.separator;
    if (!separator) {
        return barcode;
    }
    try {
        return barcode.replace(new RegExp(separator, "g"), GS1_SEPARATOR);
    } catch {
        // An invalid separator regex in the nomenclature: leave the scan as is.
        return barcode;
    }
}

/** The rule that defines `ai`, or null. */
function ruleForAi(ai, rules) {
    for (const rule of rules) {
        const match = rule.aiRegex.exec(ai);
        if (match && match[0].length === ai.length) {
            return rule;
        }
    }
    return null;
}

/**
 * Read a token's value the way its rule says to: a numeric identifier is only
 * accepted when its check digit is right, a date becomes an ISO date, and a
 * measure gets its decimal point from the last digit of the AI.
 */
function readValue(token) {
    const {rule, ai, value} = token;
    switch (rule && rule.contentType) {
        case "identifier":
            if (!hasValidCheckDigit(value)) {
                return {error: `Invalid GS1 check digit for AI ${ai}`};
            }
            return {value};
        case "date": {
            const date = toISODate(value);
            return date ? {value: date} : {error: `Invalid GS1 date for AI ${ai}`};
        }
        case "measure": {
            const decimals = rule.decimalUsage ? parseInt(ai.slice(-1), 10) : 0;
            let amount = value;
            let currency = null;
            // AI 391n and 393n put the ISO 4217 currency code before the amount.
            if (rule.type === "price" && /^39[13]/.test(ai) && amount.length > 3) {
                currency = amount.slice(0, 3);
                amount = amount.slice(3);
            }
            const digits = parseInt(amount, 10);
            if (!Number.isFinite(digits)) {
                return {error: `Invalid GS1 measure for AI ${ai}`};
            }
            return {
                value: decimals > 0 ? digits / Math.pow(10, decimals) : digits,
                currency,
            };
        }
        default:
            return {value};
    }
}

/**
 * Whether the element found at a position may be taken as the end of the
 * variable-length value that precedes it, when a separator was dropped.
 *
 * Only a specific, non-alphanumeric identifier qualifies. A digit sequence in a
 * lot number happens to look like plenty of identifiers -- an alphanumeric lot
 * such as "L0892611" contains "92", and a catch-all measure range matches
 * almost any four digits -- and breaking there silently invents a quantity or
 * truncates the lot. The element must also read cleanly: a value, a real date,
 * a right check digit.
 */
function canEndValue(match) {
    return (
        Boolean(match) &&
        !match.rule.generic &&
        match.rule.contentType !== "alpha" &&
        match.value !== "" &&
        !readValue(match).error
    );
}

/**
 * Where a variable-length value ends.
 *
 * GS1 ends it at the FNC1 separator, or at the end of the barcode when it is
 * the last element -- where no separator is needed, and where GS1 recommends
 * putting it. That reading comes first. Only when it is impossible -- the value
 * would be longer than its rule allows, or not match it -- was a separator
 * dropped, and the value is then ended at the next element that may end it.
 * `matchAt(index)` returns the rule match at a position, as `matchRule` does.
 */
function findVariableEnd(barcode, start, ai, rule, matchAt) {
    const separatorIndex = barcode.indexOf(GS1_SEPARATOR, start);
    const end = separatorIndex === -1 ? barcode.length : separatorIndex;
    const maxLength = rule.maxLength || 20;
    if (
        end - start <= maxLength &&
        rule.fullRegex.test(ai + barcode.slice(start, end))
    ) {
        return end;
    }
    const maxIndex = Math.min(end, start + maxLength);
    for (let index = start + 1; index < maxIndex; index++) {
        if (canEndValue(matchAt(index))) {
            return index;
        }
    }
    return maxIndex;
}

/**
 * The first rule that matches at `index`, with the value it captures.
 *
 * Finding where a variable-length value ends looks ahead with this same
 * function, so the answer for each position is kept in `cache` for the whole
 * barcode: without it an alphanumeric run such as "10A10A…" is read again at
 * every level of the look-ahead, and the time grows exponentially.
 */
function matchRule(barcode, index, rules, cache = new Map()) {
    if (cache.has(index)) {
        return cache.get(index);
    }
    const matchAt = (position) => matchRule(barcode, position, rules, cache);
    let result = null;
    const rest = barcode.slice(index);
    for (const rule of rules) {
        const aiMatch = rule.aiRegex.exec(rest);
        if (!aiMatch) {
            continue;
        }
        const ai = aiMatch[0];
        const valueStart = index + ai.length;
        let valueEnd = null;
        if (rule.fixedLength) {
            valueEnd = valueStart + rule.fixedLength;
            if (valueEnd > barcode.length) {
                continue;
            }
        } else {
            valueEnd = findVariableEnd(barcode, valueStart, ai, rule, matchAt);
        }
        const value = barcode.slice(valueStart, valueEnd);
        if (!rule.fullRegex.test(ai + value)) {
            continue;
        }
        result = {rule, ai, value, end: valueEnd};
        break;
    }
    cache.set(index, result);
    return result;
}

function parseParenthesizedGS1(barcode, rules) {
    const tokenRegex = /\((\d{2,4})\)([^()]*)/g;
    const tokens = [];
    let match = null;
    while ((match = tokenRegex.exec(barcode)) !== null) {
        const ai = match[1];
        tokens.push({rule: ruleForAi(ai, rules), ai, value: match[2].trim()});
    }
    return {tokens, rest: ""};
}

function parseRawGS1(barcode, rules) {
    const tokens = [];
    const cache = new Map();
    let index = 0;
    while (index < barcode.length) {
        if (barcode[index] === GS1_SEPARATOR) {
            index += 1;
            continue;
        }
        const match = matchRule(barcode, index, rules, cache);
        if (!match) {
            break;
        }
        tokens.push({rule: match.rule, ai: match.ai, value: match.value});
        index = match.end;
    }
    return {tokens, rest: barcode.slice(index).replaceAll(GS1_SEPARATOR, "")};
}

/**
 * The measure that stands for the goods themselves: the first trade measure
 * whose unit is known, otherwise the first trade measure. A logistic measure
 * (the gross weight of the pack, say) never does.
 */
function goodsMeasure(measures) {
    const trade = measures.filter((measure) => !LOGISTIC_MEASURE_AI.test(measure.ai));
    return trade.find((measure) => measure.uom) || trade[0] || null;
}

/**
 * Decode a GS1 barcode into structured fields.
 *
 * The result follows the conventions the app already reads: `value`/`product`
 * hold the product code (screens and scan handlers look the product up with
 * it), `qty`/`quantity` the piece count the barcode states — null when it
 * states none, so the screen applies its own default: a single unit, or the
 * pack's quantity for a packaging barcode — and `lot`/`serial`/`expiration` the
 * tracking data. A GS1 scan therefore flows through the existing screens
 * without them knowing anything about GS1.
 *
 * Every measure the barcode carries is listed in `measures`, and the one that
 * stands for the goods (a net weight, say, never the gross weight of the pack)
 * is kept in `weight`/`weightUom`. None of them becomes the quantity here:
 * whether one is depends on the unit the product is stocked in, which only the
 * warehouse knows.
 *
 * What each application identifier means comes from Odoo's GS1 nomenclature
 * when one is configured, so a rule added in Settings is honoured here too.
 */
export function parseGS1Barcode(barcode) {
    const normalized = applyAlternativeSeparators(normalizeBarcode(barcode));
    const rules = activeRules();
    const {tokens, rest} = PARENTHESISED_AI.test(normalized)
        ? parseParenthesizedGS1(normalized, rules)
        : parseRawGS1(normalized, rules);

    const parsed = {
        type: "gs1",
        barcode: normalized,
        value: null,
        ais: {},
        gtin: null,
        product: null,
        productCodes: [],
        sscc: null,
        packageType: null,
        lot: null,
        serial: null,
        expiration: null,
        expiry: null,
        useDate: null,
        packDate: null,
        productionDate: null,
        location: null,
        locationDest: null,
        weight: null,
        weightUom: null,
        measures: [],
        count: null,
        price: null,
        currency: null,
        qty: null,
        quantity: null,
        errors: [],
    };
    let hasExpiration = false;
    let rejectedGtin = false;

    for (const token of tokens) {
        parsed.ais[token.ai] = token.value;
        if (!token.rule) {
            parsed.errors.push(`Unknown GS1 application identifier ${token.ai}`);
            continue;
        }
        if (!token.rule.fullRegex.test(token.ai + token.value)) {
            // Only a parenthesised value can get here: the raw reading never
            // cuts a value its rule would not accept.
            parsed.errors.push(`Invalid GS1 value for AI ${token.ai}`);
            rejectedGtin = rejectedGtin || token.rule.type === "product";
            continue;
        }
        const read = readValue(token);
        if (read.error) {
            parsed.errors.push(read.error);
            rejectedGtin = rejectedGtin || token.rule.type === "product";
            continue;
        }
        const value = read.value;

        switch (token.rule.type) {
            case "product":
                // The trade item (AI 01) wins over the items it contains (02).
                parsed.gtin = parsed.gtin || value;
                break;
            case "package":
                parsed.sscc = value;
                break;
            case "package_type":
                parsed.packageType = value;
                break;
            case "lot":
                if (token.ai === "21") {
                    parsed.serial = value;
                    parsed.lot = parsed.lot || value;
                } else {
                    parsed.lot = value;
                }
                break;
            case "quantity":
                if (token.rule.decimalUsage) {
                    parsed.measures.push({ai: token.ai, value, uom: token.rule.uom});
                } else {
                    parsed.count = value;
                    parsed.qty = value;
                    parsed.quantity = value;
                }
                break;
            case "weight":
                // A rule configured as a weighted product: a measure, exactly
                // like a variable-weight one.
                parsed.measures.push({ai: token.ai, value, uom: token.rule.uom});
                break;
            case "price":
                parsed.price = value;
                parsed.currency = read.currency || parsed.currency;
                break;
            case "expiration_date":
                parsed.expiration = value;
                parsed.expiry = value;
                hasExpiration = true;
                break;
            case "use_date":
                parsed.useDate = value;
                if (!hasExpiration) {
                    parsed.expiration = value;
                    parsed.expiry = value;
                }
                break;
            case "pack_date":
                parsed.packDate = value;
                break;
            case "production_date":
                parsed.productionDate = value;
                break;
            case "location":
                parsed.location = value;
                break;
            case "location_dest":
                parsed.locationDest = value;
                break;
        }
    }

    const measure = goodsMeasure(parsed.measures);
    if (measure) {
        parsed.weight = measure.value;
        parsed.weightUom = measure.uom;
    }
    if (rest) {
        parsed.errors.push(`Unparsed GS1 data "${rest}"`);
    }
    if (parsed.gtin) {
        parsed.productCodes = gtinVariants(parsed.gtin);
        [parsed.value] = parsed.productCodes;
        parsed.product = parsed.value;
    } else if (!rejectedGtin) {
        parsed.errors.push("Missing GTIN (AI 01)");
    }

    return parsed;
}

/**
 * How a barcode shows itself to be GS1 data. A symbology identifier, an FNC1
 * separator or a parenthesised application identifier is proof. A raw string
 * starting with the GTIN AI (01) and longer than an EAN13 is only a hint, which
 * the parse has to confirm. Anything else is not GS1 data.
 */
function gs1Evidence(barcode) {
    const raw = String(barcode || "").trim();
    if (GS1_SYMBOLOGIES.some((identifier) => raw.startsWith(identifier))) {
        return "proof";
    }
    const normalized = normalizeBarcode(barcode);
    if (PARENTHESISED_AI.test(normalized) || normalized.includes(GS1_SEPARATOR)) {
        return "proof";
    }
    if (normalized.startsWith("01") && normalized.length > 13) {
        return "hint";
    }
    return null;
}

/**
 * True if the barcode may be GS1 data: proof of it, or the hint of a raw string
 * starting with the GTIN AI (01) that is longer than a plain EAN13 (so genuine
 * EAN13 codes fall through to the base parser).
 */
export function isGS1Barcode(barcode) {
    return gs1Evidence(barcode) !== null;
}

/**
 * Registered barcode parser. Only claims GS1 data; returns null otherwise so
 * the base EAN13 fallback (and any other parser) can handle the scan. A code
 * that only hinted at GS1 and yields no application identifier at all — an
 * ITF-14 with indicator digit 0, an internal reference starting with "01" — is
 * not GS1 data either.
 */
export function parseGs1(barcode) {
    const evidence = gs1Evidence(barcode);
    if (!evidence) {
        return null;
    }
    const parsed = parseGS1Barcode(barcode);
    if (evidence === "hint" && !Object.keys(parsed.ais).length) {
        return null;
    }
    return parsed;
}

barcodeParsers.add("gs1", parseGs1, {sequence: 10});
