import {BarcodeParser} from "@barcodes/js/barcode_parser";

/**
 * The GS1 rules the parser works with come from Odoo's own nomenclature
 * (`barcode.nomenclature` / `barcode.rule`, as shipped and extended by the
 * standard `barcodes_gs1_nomenclature` module), so an administrator can add or
 * adapt an application identifier from Settings instead of us hard-coding it.
 *
 * The scan path is synchronous, so the rules are fetched once when the app
 * starts and cached here. Until they are loaded — or if no GS1 nomenclature is
 * configured — the parser falls back to its built-in application identifiers.
 */

const NOMENCLATURE_FIELDS = ["name", "is_gs1_nomenclature", "gs1_separator_fnc1"];
const RULE_FIELDS = [
    "name",
    "sequence",
    "type",
    "pattern",
    "gs1_content_type",
    "gs1_decimal_usage",
    "associated_uom_id",
];

// Every rule pattern starts with the application identifier group, e.g.
// "(310[0-5])(\d{6})" -> AI "310[0-5]", value "\d{6}".
const AI_GROUP = /^\(([^()]*)\)/;
// A value group is variable-length as soon as it carries an open quantifier.
const VARIABLE_QUANTIFIER = /[*+?]|\{\d*,\d*\}/;
const FIXED_QUANTIFIER = /\{(\d+)\}\)?$/;
const OPEN_QUANTIFIER = /\{\d*,(\d+)\}\)?$/;

// Only used for `get_barcode_check_digit`, which is plain arithmetic on a
// string: no nomenclature needed.
const checkDigitParser = new BarcodeParser({});

let cachedNomenclature = null;

/**
 * The GS1 check digit (modulo 10) of a numeric identifier, computed the way
 * Odoo does — the value is zero-padded to 18 digits first, so the same
 * algorithm covers a GLN (13), a GTIN (14) and an SSCC (18).
 */
export function gs1CheckDigit(value) {
    return checkDigitParser.get_barcode_check_digit(String(value).padStart(18, "0"));
}

/** True if the last digit of a numeric identifier matches its check digit. */
export function hasValidCheckDigit(value) {
    const digits = String(value || "");
    if (!/^\d{2,18}$/.test(digits)) {
        return false;
    }
    return gs1CheckDigit(digits) === parseInt(digits.slice(-1), 10);
}

/**
 * Turn a `barcode.rule` record into what the parser needs: how to recognise the
 * application identifier, how long its value is, and how to read that value.
 *
 * Returns null for a pattern we cannot make sense of, so one broken custom rule
 * cannot take the whole parser down with it.
 */
export function compileGs1Rule(rule) {
    const pattern = rule.pattern || "";
    const aiMatch = AI_GROUP.exec(pattern);
    if (!aiMatch) {
        return null;
    }
    const valuePattern = pattern.slice(aiMatch[0].length);
    const fixed = FIXED_QUANTIFIER.exec(valuePattern);
    const open = OPEN_QUANTIFIER.exec(valuePattern);
    const variable = VARIABLE_QUANTIFIER.test(valuePattern);
    try {
        return {
            name: rule.name,
            type: rule.type,
            contentType: rule.gs1_content_type,
            decimalUsage: Boolean(rule.gs1_decimal_usage),
            // Catch-all built-ins (a whole AI range in one pattern) match too
            // eagerly to be trusted as the boundary of a variable-length value.
            generic: Boolean(rule.generic),
            // The unit a measure is expressed in (AI 310n is kilograms, 320n
            // pounds, ...), which is what tells a measure apart from a count.
            uom: rule.associated_uom_id
                ? {id: rule.associated_uom_id[0], name: rule.associated_uom_id[1]}
                : null,
            aiRegex: new RegExp(`^(?:${aiMatch[1]})`),
            fullRegex: new RegExp(`^${pattern}$`),
            fixedLength: variable ? null : (fixed && parseInt(fixed[1], 10)) || null,
            maxLength: variable ? (open && parseInt(open[1], 10)) || 20 : null,
        };
    } catch {
        // An invalid regex in a user-edited rule: skip it.
        return null;
    }
}

/** The cached GS1 nomenclature, or null while none is loaded. */
export function getGs1Nomenclature() {
    return cachedNomenclature;
}

/** Set the cached nomenclature. Used by the loader and by the tests. */
export function setGs1Nomenclature(nomenclature) {
    cachedNomenclature = nomenclature;
}

/** Compile a nomenclature record and its rules into what the parser reads. */
export function compileGs1Nomenclature(nomenclature, rules) {
    return {
        id: nomenclature.id,
        name: nomenclature.name,
        separator: nomenclature.gs1_separator_fnc1 || null,
        rules: rules
            .slice()
            .sort((left, right) => (left.sequence || 0) - (right.sequence || 0))
            .map(compileGs1Rule)
            .filter(Boolean),
    };
}

async function findGs1Nomenclature(orm, companyId) {
    // The company's own nomenclature comes first: it is the one the rest of
    // Odoo parses with. Any other GS1 nomenclature is a fallback, so the module
    // still works when the company is left on the default (non-GS1) one.
    if (companyId) {
        const [company] = await orm.read(
            "res.company",
            [companyId],
            ["nomenclature_id"]
        );
        const nomenclatureId = company?.nomenclature_id && company.nomenclature_id[0];
        if (nomenclatureId) {
            const [nomenclature] = await orm.read(
                "barcode.nomenclature",
                [nomenclatureId],
                NOMENCLATURE_FIELDS
            );
            if (nomenclature && nomenclature.is_gs1_nomenclature) {
                return nomenclature;
            }
        }
    }
    const [nomenclature] = await orm.searchRead(
        "barcode.nomenclature",
        [["is_gs1_nomenclature", "=", true]],
        NOMENCLATURE_FIELDS,
        {limit: 1}
    );
    return nomenclature || null;
}

/**
 * Fetch the GS1 nomenclature and its GS1-128 rules, and cache them for the
 * parser. Returns the cached nomenclature, or null when there is none to use —
 * including when it cannot be read, so the parser falls back to its built-in
 * identifiers instead of a half-read nomenclature.
 */
export async function loadGs1Nomenclature(orm, companyId) {
    try {
        const nomenclature = await findGs1Nomenclature(orm, companyId);
        if (!nomenclature) {
            setGs1Nomenclature(null);
            return null;
        }
        const rules = await orm.searchRead(
            "barcode.rule",
            [
                ["barcode_nomenclature_id", "=", nomenclature.id],
                ["encoding", "=", "gs1-128"],
            ],
            RULE_FIELDS,
            {order: "sequence"}
        );
        setGs1Nomenclature(compileGs1Nomenclature(nomenclature, rules));
    } catch {
        setGs1Nomenclature(null);
    }
    return getGs1Nomenclature();
}
