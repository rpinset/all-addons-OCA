/** @odoo-module **/

import {afterEach, describe, expect, test} from "@odoo/hoot";
import {gtinVariants, isGS1Barcode, parseGs1} from "@barcode_gs1/js/gs1_parser.esm";
import {
    compileGs1Nomenclature,
    getGs1Nomenclature,
    hasValidCheckDigit,
    loadGs1Nomenclature,
    setGs1Nomenclature,
} from "@barcode_gs1/js/gs1_nomenclature.esm";
import {parseBarcode} from "@barcode_scanner/js/barcode_parser.esm";

// FNC1 (<GS>, 0x1D), the separator a scanner sends between variable-length AIs.
const GS = String.fromCharCode(29);
// The characters GS1 allows in an alphanumeric value.
const ALPHA = '[!"%-/0-9:-?A-Z_a-z]';

// The GS1 rules Odoo ships in `barcodes_gs1_nomenclature`, trimmed to what
// these tests exercise.
const ODOO_RULES = [
    {
        name: "SSCC",
        sequence: 1,
        pattern: "(00)(\\d{18})",
        type: "package",
        gs1_content_type: "identifier",
    },
    {
        name: "GTIN",
        sequence: 2,
        pattern: "(01)(\\d{14})",
        type: "product",
        gs1_content_type: "identifier",
    },
    {
        name: "Physical location GLN",
        sequence: 6,
        pattern: "(414)(\\d{13})",
        type: "location",
        gs1_content_type: "identifier",
    },
    {
        name: "Batch or lot number",
        sequence: 10,
        pattern: `(10)(${ALPHA}{0,20})`,
        type: "lot",
        gs1_content_type: "alpha",
    },
    {
        name: "Serial number",
        sequence: 11,
        pattern: `(21)(${ALPHA}{0,20})`,
        type: "lot",
        gs1_content_type: "alpha",
    },
    {
        name: "Expiration date",
        sequence: 15,
        pattern: "(17)(\\d{6})",
        type: "expiration_date",
        gs1_content_type: "date",
    },
    {
        name: "Variable count of items",
        sequence: 20,
        pattern: "(30)(\\d{0,8})",
        type: "quantity",
        gs1_content_type: "measure",
        gs1_decimal_usage: false,
    },
    {
        name: "Net weight, kilograms",
        sequence: 21,
        pattern: "(310[0-5])(\\d{6})",
        type: "quantity",
        gs1_content_type: "measure",
        gs1_decimal_usage: true,
    },
];

const KG = [13, "kg"];

function loadNomenclature(rules, separator = "(Alt029|#|\\x1D)") {
    setGs1Nomenclature(
        compileGs1Nomenclature(
            {id: 1, name: "Default GS1 Nomenclature", gs1_separator_fnc1: separator},
            rules
        )
    );
}

describe("BarcodeGs1", () => {
    // The nomenclature is cached for the whole session; each test starts from
    // the built-in identifiers unless it loads its own rules.
    afterEach(() => setGs1Nomenclature(null));

    test("a parenthesised barcode decodes the GTIN, the lot and the expiry", () => {
        expect(parseGs1("(01)09501101020917(10)LOT123(17)261231")).toMatchObject({
            type: "gs1",
            value: "9501101020917",
            gtin: "09501101020917",
            lot: "LOT123",
            expiration: "2026-12-31",
            expiry: "2026-12-31",
            qty: null,
            errors: [],
        });
    });

    test("a raw FNC1-separated barcode decodes the same fields", () => {
        expect(parseGs1(`0109501101020917${GS}10LOT123${GS}17261231`)).toMatchObject({
            value: "9501101020917",
            lot: "LOT123",
            expiry: "2026-12-31",
            errors: [],
        });
    });

    test("a variable-length value runs to the end when it is the last element", () => {
        // GS1 needs no separator after the last element, and recommends putting
        // the variable-length ones there: digits inside the value that look
        // like an identifier must not cut it short.
        expect(parseGs1("0109501101020917215830192")).toMatchObject({
            serial: "5830192",
            lot: "5830192",
            count: null,
            qty: null,
            errors: [],
        });
        expect(parseGs1("0109501101020917214711000123")).toMatchObject({
            serial: "4711000123",
            productionDate: null,
            errors: [],
        });
        expect(parseGs1("010950110102091710A3712")).toMatchObject({
            lot: "A3712",
            count: null,
            qty: null,
            errors: [],
        });
        expect(parseGs1("01095011010209171020241130")).toMatchObject({
            lot: "20241130",
            errors: [],
        });
        expect(parseGs1("01095011010209171726123110LOT123")).toMatchObject({
            lot: "LOT123",
            expiry: "2026-12-31",
            errors: [],
        });
    });

    test("a value too long to be one ends at the next element that reads cleanly", () => {
        // Longer than a lot may be, so a separator was dropped: the lot ends
        // where a real date starts, and the count after it is read as well.
        expect(parseGs1("010950110102091710LOT12345678172612313005")).toMatchObject({
            lot: "LOT12345678",
            expiry: "2026-12-31",
            count: 5,
            qty: 5,
            errors: [],
        });
        // "17991399" looks like an expiry date but is not one (month 13): the
        // lot is not cut there.
        expect(parseGs1("010950110102091710AB17991399CD172612313005")).toMatchObject({
            lot: "AB17991399CD",
            expiry: "2026-12-31",
            count: 5,
            errors: [],
        });
    });

    test("a long alphanumeric run without separators is read in linear time", () => {
        // Every "10" in the run could open another lot, so finding where each
        // value ends looks ahead again and again: without remembering what
        // each position matched, this 80-character scan takes about 25 s.
        const parsed = parseGs1("]C110" + "A10".repeat(25));
        expect(parsed.lot).toBe("A10A10A10A10A10A10A1");
        expect(parsed.errors).toInclude("Missing GTIN (AI 01)");
    });

    test("a count (AI 30) is the quantity and a serial (AI 21) doubles as the lot", () => {
        expect(parseGs1("(01)09501101020917(21)SN9(30)12")).toMatchObject({
            serial: "SN9",
            lot: "SN9",
            qty: 12,
            quantity: 12,
        });
    });

    test("a net weight (AI 310n) is decoded with its decimals, not as the quantity", () => {
        // Whether a weight is the quantity depends on the unit the product is
        // stocked in, which the parser does not know: 1.25 kg is not 1.25 units.
        expect(parseGs1("(01)09501101020917(3103)001250")).toMatchObject({
            weight: 1.25,
            count: null,
            qty: null,
            quantity: null,
        });
    });

    test("a count next to the weight is the quantity", () => {
        expect(parseGs1("(01)09501101020917(3103)001250(30)4")).toMatchObject({
            weight: 1.25,
            qty: 4,
        });
    });

    test("the gross weight of the pack never stands for the goods", () => {
        // Odoo ships the net weight (310n) with its unit, and no rule for the
        // gross weight (330n): the built-in identifier reads it, unitless.
        loadNomenclature([ODOO_RULES[1], {...ODOO_RULES[7], associated_uom_id: KG}]);
        const net = {ai: "3103", value: 2.497, uom: {id: 13, name: "kg"}};
        const gross = {ai: "3303", value: 2.7, uom: null};
        // Net and gross, in either order: the net weight is the goods'.
        for (const label of [
            "(01)09501101020917(3103)002497(3303)002700",
            "(01)09501101020917(3303)002700(3103)002497",
        ]) {
            expect(parseGs1(label)).toMatchObject({
                weight: 2.497,
                weightUom: {id: 13, name: "kg"},
            });
        }
        expect(parseGs1("(01)09501101020917(3103)002497(3303)002700").measures).toEqual(
            [net, gross]
        );
        // A gross weight alone is listed, but is no measure of the goods.
        expect(parseGs1("(01)09501101020917(3303)002700")).toMatchObject({
            weight: null,
            weightUom: null,
            measures: [gross],
        });
    });

    test("every measure is listed, the first one with a unit stands for the goods", () => {
        loadNomenclature([
            ODOO_RULES[1],
            {...ODOO_RULES[7], associated_uom_id: KG},
            {
                name: "Net volume, litres",
                sequence: 25,
                pattern: "(315[0-5])(\\d{6})",
                type: "quantity",
                gs1_content_type: "measure",
                gs1_decimal_usage: true,
                associated_uom_id: [11, "L"],
            },
        ]);
        // A width with no rule (so no unit), a net weight and a net volume.
        const parsed = parseGs1(
            "(01)09501101020917(3122)000300(3103)002497(3152)000250"
        );
        expect(parsed.measures).toEqual([
            {ai: "3122", value: 3, uom: null},
            {ai: "3103", value: 2.497, uom: {id: 13, name: "kg"}},
            {ai: "3152", value: 2.5, uom: {id: 11, name: "L"}},
        ]);
        expect(parsed).toMatchObject({weight: 2.497, weightUom: {id: 13, name: "kg"}});
    });

    test("DD=00 in a date means the last day of the month", () => {
        expect(parseGs1("(01)09501101020917(15)261200")).toMatchObject({
            expiry: "2026-12-31",
            useDate: "2026-12-31",
            errors: [],
        });
    });

    test("an expiration date (17) wins over a best-before date (15)", () => {
        expect(parseGs1("(01)09501101020917(15)261200(17)270101")).toMatchObject({
            expiry: "2027-01-01",
            useDate: "2026-12-31",
            errors: [],
        });
    });

    test("production (11) and pack (13) dates are decoded on their own fields", () => {
        expect(parseGs1("(01)09501101020917(11)260115(13)260116")).toMatchObject({
            productionDate: "2026-01-15",
            packDate: "2026-01-16",
            expiry: null,
            errors: [],
        });
    });

    test("an impossible date is reported instead of silently accepted", () => {
        const parsed = parseGs1("(01)09501101020917(17)260230");
        expect(parsed.expiry).toBe(null);
        expect(parsed.errors).toEqual(["Invalid GS1 date for AI 17"]);
    });

    test("a symbology identifier is stripped before parsing", () => {
        expect(parseGs1("]C10109501101020917")).toMatchObject({
            value: "9501101020917",
            errors: [],
        });
    });

    test("an SSCC-only label is decoded but reports the missing GTIN", () => {
        expect(parseGs1("(00)123456789012345675")).toMatchObject({
            sscc: "123456789012345675",
            value: null,
            errors: ["Missing GTIN (AI 01)"],
        });
    });

    test("a GLN identifies the physical location it was scanned for", () => {
        expect(parseGs1("(414)9501101020917")).toMatchObject({
            location: "9501101020917",
            errors: ["Missing GTIN (AI 01)"],
        });
    });

    test("a misread GTIN is refused by its check digit", () => {
        // Same barcode as above with the last digit off by one.
        expect(parseGs1("(01)09501101020916(10)LOT123")).toMatchObject({
            gtin: null,
            value: null,
            lot: "LOT123",
            errors: ["Invalid GS1 check digit for AI 01"],
        });
    });

    test("a misread SSCC or GLN is refused too", () => {
        expect(parseGs1("(00)123456789012345678")).toMatchObject({
            sscc: null,
            errors: ["Invalid GS1 check digit for AI 00", "Missing GTIN (AI 01)"],
        });
        expect(parseGs1("(414)9501101020916")).toMatchObject({
            location: null,
            errors: ["Invalid GS1 check digit for AI 414", "Missing GTIN (AI 01)"],
        });
    });

    test("the check digit is the GS1 modulo 10 of the zero-padded identifier", () => {
        expect(hasValidCheckDigit("09501101020917")).toBe(true);
        expect(hasValidCheckDigit("09501101020916")).toBe(false);
        expect(hasValidCheckDigit("123456789012345675")).toBe(true);
        expect(hasValidCheckDigit("123456789012345678")).toBe(false);
    });

    test("the GTIN resolves to the shortest form a product stores", () => {
        // GS1 pads the GTIN to 14 digits; products hold the code printed on the
        // item, which Odoo stores as an EAN13 (`sanitize_ean`).
        expect(gtinVariants("09501101020917")).toEqual([
            "9501101020917",
            "09501101020917",
        ]);
        // A UPC-A: 13 digits first, the shorter forms still offered.
        expect(gtinVariants("00012345678905")).toEqual([
            "0012345678905",
            "00012345678905",
            "012345678905",
            "12345678905",
        ]);
        // A genuine ITF-14 has no padding to strip.
        expect(gtinVariants("10012345678902")).toEqual(["10012345678902"]);
    });

    test("only GS1 data is claimed, so other codes reach the base parser", () => {
        expect(isGS1Barcode("9501101020917")).toBe(false);
        expect(parseGs1("9501101020917")).toBe(null);
        // 01... but too short to be anything but an EAN13.
        expect(parseGs1("0123456789012")).toBe(null);
        expect(isGS1Barcode("(01)09501101020917")).toBe(true);
        // An ITF-14 with indicator digit 0 starts with "01" too, but no
        // application identifier reads out of it: it is a plain code.
        expect(parseGs1("01234567890128")).toBe(null);
        // A parenthesis is not an application identifier.
        expect(isGS1Barcode("PAL(3)-A")).toBe(false);
        expect(parseGs1("PAL(3)-A")).toBe(null);
    });

    test("a parenthesised value its rule does not accept is reported, not read", () => {
        expect(parseGs1("(01)09501101020917(30)12abc")).toMatchObject({
            count: null,
            qty: null,
            errors: ["Invalid GS1 value for AI 30"],
        });
        expect(
            parseGs1("(01)09501101020917(10)ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        ).toMatchObject({lot: null, errors: ["Invalid GS1 value for AI 10"]});
        // A GTIN is always 14 digits.
        expect(parseGs1("(01)9501101020917")).toMatchObject({
            gtin: null,
            errors: ["Invalid GS1 value for AI 01"],
        });
    });

    test("what cannot be parsed is reported whole", () => {
        expect(parseGs1(`0109501101020917${GS}ZZ${GS}YY${GS}XX`).errors).toEqual([
            'Unparsed GS1 data "ZZYYXX"',
        ]);
    });

    test("a nomenclature that cannot be read leaves the built-in identifiers", async () => {
        loadNomenclature(ODOO_RULES);
        const offline = () => Promise.reject(new Error("offline"));
        const orm = {read: offline, searchRead: offline};
        expect(await loadGs1Nomenclature(orm, 1)).toBe(null);
        expect(getGs1Nomenclature()).toBe(null);
        expect(parseGs1("(01)09501101020917(11)260115")).toMatchObject({
            productionDate: "2026-01-15",
            errors: [],
        });
    });

    test("the parser is registered ahead of the built-in EAN13 fallback", () => {
        expect(parseBarcode("(01)09501101020917(10)LOT123").type).toBe("gs1");
        expect(parseBarcode("9501101020917").type).toBe("ean13");
    });

    test("Odoo's own GS1 rules decode the same fields", () => {
        loadNomenclature(ODOO_RULES);
        expect(parseGs1("(01)09501101020917(10)LOT123(17)261231")).toMatchObject({
            value: "9501101020917",
            lot: "LOT123",
            expiry: "2026-12-31",
            qty: null,
            errors: [],
        });
        expect(parseGs1(`0109501101020917${GS}10LOT123${GS}17261231`)).toMatchObject({
            value: "9501101020917",
            lot: "LOT123",
            expiry: "2026-12-31",
            errors: [],
        });
        expect(parseGs1("01095011010209171726123110LOT123")).toMatchObject({
            value: "9501101020917",
            lot: "LOT123",
            expiry: "2026-12-31",
            errors: [],
        });
        expect(parseGs1("(01)09501101020917(3103)001250")).toMatchObject({
            weight: 1.25,
            qty: null,
            errors: [],
        });
        expect(parseGs1("(01)09501101020916")).toMatchObject({
            gtin: null,
            errors: ["Invalid GS1 check digit for AI 01"],
        });
    });

    test("the nomenclature's own separator characters are accepted", () => {
        // A scanner that cannot emit FNC1 is configured to send "#" instead.
        loadNomenclature(ODOO_RULES);
        expect(parseGs1("0109501101020917#10LOT123#17261231")).toMatchObject({
            value: "9501101020917",
            lot: "LOT123",
            expiry: "2026-12-31",
            errors: [],
        });
        // A code that merely contains one of those characters is not GS1 data.
        expect(isGS1Barcode("ABC#123")).toBe(false);
        expect(parseGs1("ABC#123")).toBe(null);
    });

    test("an AI the nomenclature does not define still parses", () => {
        // Odoo ships no rule for a production date (AI 11): without the
        // built-in fallback it would cut the rest of the barcode short.
        loadNomenclature(ODOO_RULES);
        expect(parseGs1("(01)09501101020917(11)260115(10)LOT9")).toMatchObject({
            productionDate: "2026-01-15",
            lot: "LOT9",
            errors: [],
        });
        expect(parseGs1(`0109501101020917${GS}2012${GS}10LOT9`)).toMatchObject({
            lot: "LOT9",
            errors: [],
        });
    });

    test("labels off real pallets decode the same in every form", () => {
        // Cured guanciale, 2 pieces of 2.497 kg: (01)(3103)(10)(30)(15).
        const guanciale = {
            value: "98003948002568",
            lot: "534343",
            weight: 2.497,
            count: 2,
            qty: 2,
            expiry: "2026-10-06",
            errors: [],
        };
        expect(
            parseGs1("(01)98003948002568(3103)002497(10)534343(30)02(15)261006")
        ).toMatchObject(guanciale);
        expect(
            parseGs1(`0198003948002568310300249710534343${GS}3002${GS}15261006`)
        ).toMatchObject(guanciale);
        // With the separators dropped there is no telling where the lot ends:
        // GS1 reads it to the end. A scanner that cannot send FNC1 is set to
        // send the nomenclature's separator instead.
        expect(
            parseGs1("0198003948002568310300249710534343300215261006")
        ).toMatchObject({lot: "534343300215261006", count: null, expiry: null});

        // Hard cheese, 4.324 kg, no count: the lot closes the barcode.
        const cheese = {
            value: "98436038190867",
            lot: "L0892611",
            weight: 4.324,
            qty: null,
            expiry: "2026-09-26",
            errors: [],
        };
        expect(
            parseGs1("(01)98436038190867(15)260926(3103)004324(10)L0892611")
        ).toMatchObject(cheese);
        // "L0892611" contains "92", a company-internal identifier: breaking
        // there would truncate the lot to "L08".
        expect(parseGs1("019843603819086715260926310300432410L0892611")).toMatchObject(
            cheese
        );

        // Gorgonzola, weight only on the upper barcode.
        expect(parseGs1("(01)98017024009181(3102)000309")).toMatchObject({
            value: "98017024009181",
            weight: 3.09,
            qty: null,
            errors: [],
        });
        // ... and the tracking data on a second one, which carries no GTIN. A
        // GS1-128 scan announces itself with the "]C1" symbology identifier,
        // which is what makes this half a GS1 barcode rather than a plain code.
        expect(parseGs1("]C115260613" + "1026104005" + GS + "37002")).toMatchObject({
            lot: "26104005",
            count: 2,
            expiry: "2026-06-13",
            errors: ["Missing GTIN (AI 01)"],
        });
        expect(isGS1Barcode("]C1152606131026104005")).toBe(true);
    });

    test("an amount payable (AI 39xn) is decoded, with its currency", () => {
        expect(parseGs1("(01)09501101020917(3922)000150")).toMatchObject({
            price: 1.5,
            currency: null,
            errors: [],
        });
        // AI 391n and 393n open with the ISO 4217 numeric code (978 = EUR).
        expect(parseGs1("(01)09501101020917(3932)978000150")).toMatchObject({
            price: 1.5,
            currency: "978",
            errors: [],
        });
        expect(parseGs1("01095011010209173922000150")).toMatchObject({
            price: 1.5,
            errors: [],
        });
    });

    test("a rule configured as a weighted product is a measure, not the quantity", () => {
        loadNomenclature(
            [
                ODOO_RULES[1],
                {
                    name: "Net weight",
                    sequence: 2,
                    pattern: "(310[0-5])(\\d{6})",
                    type: "weight",
                    gs1_content_type: "measure",
                    gs1_decimal_usage: true,
                },
                ODOO_RULES[6],
            ],
            false
        );
        expect(parseGs1("(01)09501101020917(3103)001250")).toMatchObject({
            weight: 1.25,
            qty: null,
            quantity: null,
            errors: [],
        });
        // A counted quantity is the quantity.
        expect(parseGs1("(01)09501101020917(3103)001250(30)4")).toMatchObject({
            weight: 1.25,
            qty: 4,
            errors: [],
        });
    });

    test("a rule configured in Odoo wins over the built-in identifier", () => {
        // AI 91 is company-internal: here it is configured to carry the lot.
        loadNomenclature(
            [
                ODOO_RULES[1],
                {
                    name: "Internal lot",
                    sequence: 2,
                    pattern: "(91)([A-Z0-9]{0,10})",
                    type: "lot",
                    gs1_content_type: "alpha",
                },
            ],
            false
        );
        expect(parseGs1("(01)09501101020917(91)ABC123")).toMatchObject({
            value: "9501101020917",
            lot: "ABC123",
            errors: [],
        });
    });
});
