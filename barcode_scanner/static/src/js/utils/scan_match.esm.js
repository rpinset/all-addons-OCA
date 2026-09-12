/**
 * A physical reader can deliver a barcode with surrounding whitespace (a
 * keyboard-wedge prefix/suffix) or in a different letter case than what is
 * stored, so a raw `["barcode", "=", value]` match misses it while a manual
 * copy/paste of the same code works -- the exact asymmetry reported on
 * location scans in internal transfers. Build a tolerant match instead: trim
 * the value and compare case-insensitively with `=ilike`.
 *
 * `=ilike` treats `_` and `%` as SQL wildcards, so escape them (and the escape
 * character itself) to keep the match exact -- a stray wildcard in a barcode
 * could otherwise select the WRONG product or location.
 *
 * Returns a single-leaf domain ready for searchRead, or null when the scanned
 * value is empty so the caller can treat it as "no match".
 *
 * This lives in the scanner core so every feature module (stock, inventory,
 * ...) can match scans the same tolerant way without depending on one another.
 */
export function barcodeMatchDomain(value, field = "barcode") {
    const term = String(value ?? "").trim();
    if (!term) {
        return null;
    }
    const escaped = term.replace(/([\\%_])/g, "\\$1");
    return [[field, "=ilike", escaped]];
}

/**
 * Match ANY of several candidate codes the same tolerant way. A GS1 scan yields
 * a GTIN that has several equivalent forms (14/13/12-digit variants); the
 * product's stored barcode may be any one of them, so matching only the first
 * variant misses the others. This ORs a tolerant leaf per candidate.
 *
 * Accepts strings and/or arrays of strings, de-duplicates, and drops empties.
 * Returns a searchRead-ready domain, or null when there is nothing to match.
 */
export function barcodeMatchAnyDomain(values, field = "barcode") {
    const terms = [];
    for (const v of [].concat(values ?? [])) {
        const term = String(v ?? "").trim();
        if (term && !terms.includes(term)) {
            terms.push(term);
        }
    }
    if (!terms.length) {
        return null;
    }
    const leaves = terms.map((t) => [field, "=ilike", t.replace(/([\\%_])/g, "\\$1")]);
    // OR the leaves together: N leaves need N-1 leading "|" operators.
    return Array(leaves.length - 1)
        .fill("|")
        .concat(leaves);
}
