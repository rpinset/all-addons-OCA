import {roundDecimals, roundPrecision} from "@web/core/utils/numbers";
import {BarcodeScannerState} from "@barcode_stock/js/services/barcode_scanner_state.esm";
import {barcodeStartupTasks} from "@barcode_scanner/js/registries.esm";
import {patch} from "@web/core/utils/patch";

// Logistic measures (AI 330n-349n: the gross weight, dimensions and volume of
// the logistic unit) describe the pack, never the goods picked.
const LOGISTIC_MEASURE_AI = /^3[34]/;

/**
 * The measures of the goods a scan carries, in the order the label states them:
 * every one `barcode_gs1` lists in `measures`, or the single `weight`/`weightUom`
 * pair a scan without that list carries.
 */
function goodsMeasures(scan) {
    if (Array.isArray(scan?.measures)) {
        return scan.measures.filter(
            (measure) => !LOGISTIC_MEASURE_AI.test(measure.ai || "")
        );
    }
    if (scan?.weight === null || scan?.weight === undefined) {
        return [];
    }
    return [{value: scan.weight, uom: scan.weightUom}];
}

/**
 * Read the quantity of a GS1 scan the way the warehouse means it.
 *
 * A GS1 label states both a piece count (AI 30/37) and, for goods sold by
 * weight, a measure (AI 310n and friends) — a box of cured meat carries "2
 * pieces" and "2.497 kg". Neither `barcode_gs1`, which only decodes, nor
 * `barcode_stock`, which knows nothing of GS1, can decide which one is the
 * quantity picked: that depends on the unit the product is stocked in, so it is
 * decided here.
 */
patch(BarcodeScannerState.prototype, {
    /**
     * Fetch every unit of measure once, with the number of decimals a quantity
     * is stored with. There are a handful of units, they are needed to compare
     * a measure with a product, and the scan path itself is synchronous — so
     * they are warmed up when the app starts.
     */
    async loadUoms() {
        if (this.uomsById && Object.keys(this.uomsById).length) {
            return this.uomsById;
        }
        const [uoms, digits] = await Promise.all([
            this.orm.searchRead(
                "uom.uom",
                [],
                ["name", "category_id", "factor", "rounding"]
            ),
            // The decimals of "Product Unit of Measure", as a quantity field
            // that is stored with them states them. Not from precision_get over
            // RPC: once `account` is installed it overrides that method without
            // @api.model, and the call then takes the precision's name for ids.
            this.orm
                .call("stock.move.line", "fields_get", [["quantity"]], {
                    attributes: ["digits"],
                })
                .then((fields) => fields?.quantity?.digits?.[1])
                .catch(() => null),
        ]);
        this.quantityDigits = Number.isInteger(digits) ? digits : null;
        this.uomsById = Object.fromEntries(uoms.map((uom) => [uom.id, uom]));
        return this.uomsById;
    },

    /**
     * Load the units again, in the background, when loading them at startup
     * failed (a dropped connection, say) and a scan carries a measure. That scan
     * keeps the base reading; the next ones read their measure.
     */
    retryLoadUoms(scan) {
        if (this.uomsById || this.uomsRetry || !goodsMeasures(scan).length) {
            return;
        }
        this.uomsRetry = this.loadUoms()
            .catch(() => null)
            .finally(() => {
                this.uomsRetry = null;
            });
    },

    /**
     * The first measure of the goods whose unit is the kind the product is
     * stocked in, with that unit: a net volume for a product in litres, even when
     * the label states a net weight first.
     */
    matchingMeasure(scan, productUom) {
        for (const measure of goodsMeasures(scan)) {
            const value = parseFloat(measure.value);
            const uom = this.uomsById[measure.uom?.id];
            if (
                Number.isFinite(value) &&
                uom?.category_id?.[0] === productUom.category_id?.[0]
            ) {
                return {value, uom};
            }
        }
        return null;
    },

    /**
     * The measure a GS1 label carries, as a quantity of the product: converted
     * into the unit the product is stocked in, and rounded the way the server
     * will store it. Null when the label has no measure of the kind the product
     * is stocked in (a weight for a product counted in units), when the units
     * could not be read, or when the measure rounds to nothing: a quantity of
     * zero picks nothing, so the scan reads as one without a measure.
     */
    measureQuantity(scan, productUomId) {
        if (!this.uomsById) {
            this.retryLoadUoms(scan);
            return null;
        }
        const productUom = this.uomsById[productUomId];
        const measure = productUom && this.matchingMeasure(scan, productUom);
        if (!measure) {
            return null;
        }
        // Odoo's factor is how many of a unit make one unit of its category's
        // reference, so converting is a ratio of the two.
        const quantity = this.roundAsStored(
            (measure.value / (measure.uom.factor || 1)) * (productUom.factor || 1),
            productUom
        );
        return quantity > 0 ? quantity : null;
    },

    /**
     * A quantity in `uom` as the server will store it. What lands in stock is
     * rounded to the unit's rounding and to the decimals of "Product Unit of
     * Measure": with the defaults (0.01 kg, two decimals) the 2.497 kg a label
     * states is stored as 2.50. Rounding here too shows the quantity that will
     * be stored, not one that will change once saved.
     */
    roundAsStored(quantity, uom) {
        let rounded =
            uom.rounding > 0 ? roundPrecision(quantity, uom.rounding) : quantity;
        if (Number.isInteger(this.quantityDigits)) {
            rounded = roundDecimals(rounded, this.quantityDigits);
        }
        return rounded;
    },

    /**
     * @override
     * The measure becomes the quantity when its unit is the kind the product is
     * stocked in. Otherwise the base reading stands: the piece count on the
     * label, or a single unit when it states none — a weight must never turn
     * into a number of units.
     */
    scannedQuantity(scan, productUomId) {
        const measured = this.measureQuantity(scan, productUomId);
        return measured === null ? super.scannedQuantity(...arguments) : measured;
    },

    /**
     * @override
     * A packaging barcode stands for a whole pack, and the base takes the pack's
     * quantity whenever the label states no count. A measure is more precise
     * than that: a carton of cheese weighing 4.32 kg is 4.32 for a product
     * stocked in kilograms, not the pack's nominal quantity.
     */
    applyScanResult(scan) {
        const result = super.applyScanResult(...arguments);
        const productId = result.candidates?.[0]?.product_id?.[0];
        const measured = this.measureQuantity(
            scan,
            this.productsById?.[productId]?.uom_id?.[0]
        );
        if (measured !== null) {
            result.quantity = measured;
        }
        return result;
    },
});

barcodeStartupTasks.add("gs1_stock_uoms", (env) =>
    env.services.barcodeScannerState.loadUoms()
);
