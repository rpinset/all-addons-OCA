import {barcodeParsers} from "@barcode_scanner/js/registries.esm";

/**
 * Built-in EAN13 parser. Registered last (high sequence) so it acts as the
 * fallback once richer parsers (e.g. GS1) have had their turn.
 */
export function parseEan13(barcode) {
    if (!/^\d{13}$/.test(barcode)) {
        return null;
    }
    return {type: "ean13", value: barcode};
}

barcodeParsers.add("ean13", parseEan13, {sequence: 100});

/**
 * Parse a scanned barcode by running the registered parsers in `sequence`
 * order and returning the first non-null result. Feature modules register
 * richer parsers ahead of the built-in EAN13 fallback via `barcode_parsers`.
 */
export function parseBarcode(barcode) {
    for (const parser of barcodeParsers.getAll()) {
        const result = parser(barcode);
        if (result) {
            return result;
        }
    }
    return null;
}
