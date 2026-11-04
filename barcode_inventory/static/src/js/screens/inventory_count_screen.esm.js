import {Component, onWillStart, useState} from "@odoo/owl";
import {ConfirmationDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {_t} from "@web/core/l10n/translation";
import {barcodeMatchAnyDomain} from "@barcode_scanner/js/utils/scan_match.esm";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {formatFloat} from "@web/core/utils/numbers";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useService} from "@web/core/utils/hooks";

/**
 * Only storable products have stock to count. A service, a non-storable
 * consumable or a combo has no quant, and Odoo refuses to create one when the
 * adjustment is applied, so they are kept out of the count from the start.
 */
export const COUNTABLE_PRODUCTS = [["is_storable", "=", true]];

/**
 * What the operator is told when the product scanned has no stock to count.
 *
 * @param {Object} product the product scanned
 * @returns {String} the message
 */
export function notStorableMessage(product) {
    return _t("%(name)s is not a storable product: it has no stock to count.", {
        name: product.display_name,
    });
}

/**
 * Count step of an inventory adjustment. Shows the stock the location holds,
 * one line per product and lot; the operator counts by scanning (a GS1 label
 * also brings its lot/serial and piece count), by adding a product from the
 * "+" product selector -- like the back office, so a product not yet in the
 * location can be added -- and by typing the counted quantity. Lot/serial
 * tracked lines without a lot get a lot field (suggesting the product's lots;
 * the server finds or creates the lot by name). Applying builds and closes a
 * stock_inventory adjustment.
 *
 * The count in progress survives the round-trip to the product selector: it is
 * carried through the navigation params and restored on the way back.
 */
export class InventoryCountScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this._seq = 0;
        this.state = useState({
            locationId: null,
            locationName: "",
            lines: [],
            loading: true,
            applying: false,
        });

        useBarcodeHandler({
            onScan: async (barcode, parsedData) => {
                await this.onBarcodeScanned(barcode, parsedData);
            },
        });

        onWillStart(async () => {
            const params = this.props.params || {};
            this.state.locationId = params.locationId || null;
            this.state.locationName = params.locationName || "";
            if (Array.isArray(params.lines)) {
                // Coming back from the product selector: restore the count.
                this.state.lines = params.lines.map((l) => ({...l}));
                this._seq = this.state.lines.reduce(
                    (max, l) => Math.max(max, l._id || 0),
                    0
                );
                this.state.loading = false;
                if (params.addProduct) {
                    await this.addOrIncrement(params.addProduct, null, null);
                }
            } else {
                await this.loadLines();
            }
        });
    }

    lineKey(productId, lotName) {
        return `${productId}|${lotName || ""}`;
    }

    async loadLines() {
        if (!this.state.locationId) {
            this.state.loading = false;
            return;
        }
        const data = await this.inventory.call(
            "stock.inventory",
            "action_barcode_location_lines",
            [this.state.locationId]
        );
        this.state.lines = (data.lines || []).map((line) => ({
            _id: ++this._seq,
            ...line,
            // Stock already here has its lot resolved; the operator just counts.
            lot_fixed: line.tracking !== "none" && Boolean(line.lot_name),
            lot_options: [],
            counted: null,
            isNew: false,
            // The stock the count is checked against when applied: what the
            // screen showed as counting began (see showStockChanges).
            checked_qty: line.theoretical_qty,
        }));
        this.state.loading = false;
    }

    // --- scanning -------------------------------------------------------------

    async onBarcodeScanned(barcode, parsed) {
        if (this.waitForApply()) {
            return;
        }
        const product = await this.findScannedProduct(barcode, parsed);
        // The count may have been applied while the product was looked up.
        if (!product || this.waitForApply()) {
            return;
        }
        const lotName = parsed?.lot || parsed?.serial || null;
        const qty = this.scannedQuantity(parsed, product.uom_id?.[0]);
        if (qty === null) {
            this.inventory.notify(
                _t("The quantity on the label of %(name)s cannot be read.", {
                    name: product.display_name,
                }),
                {type: "warning"}
            );
            return;
        }
        await this.addOrIncrement(product, lotName, qty);
    }

    /**
     * Whether the count is on its way to the server, telling the operator so:
     * a scan now would show up as counted without being so, then vanish with
     * the screen.
     *
     * @returns {Boolean} whether the scan must wait
     */
    waitForApply() {
        if (!this.state.applying) {
            return false;
        }
        this.inventory.notify(_t("Wait until the count is applied to scan again."), {
            type: "warning",
        });
        return true;
    }

    /**
     * The product a scan names, matched the same tolerant, all-candidates way
     * the other screens do: a GS1 GTIN has several equivalent variant forms,
     * and the parser's value can differ from the raw scan. When it names none
     * that can be counted, the operator is told why and null comes back.
     *
     * @param {String} barcode the raw scan
     * @param {Object} [parsed] what the parsers read from it
     * @returns {Promise<Object|null>} the product to count, if any
     */
    async findScannedProduct(barcode, parsed) {
        const candidates = [
            ...(parsed?.productCodes || []),
            parsed?.gtin,
            parsed?.value,
            barcode,
        ];
        const domain = barcodeMatchAnyDomain(candidates);
        const products = domain
            ? await this.inventory.searchRead("product.product", domain, [
                  "id",
                  "display_name",
                  "tracking",
                  "uom_id",
                  "is_storable",
              ])
            : [];
        if (!products.length) {
            this.inventory.notify(
                _t("No product matches “%(code)s”.", {code: parsed?.value || barcode}),
                {type: "warning"}
            );
            return null;
        }
        // Say why a scanned service or consumable is refused, rather than
        // "no match" for a product the operator can see in the catalogue.
        const product = products.find((p) => p.is_storable);
        if (!product) {
            this.inventory.notify(notStorableMessage(products[0]), {type: "warning"});
            return null;
        }
        return product;
    }

    /**
     * How much of the product a scan stands for: the piece count the barcode
     * states (a GS1 count, AI 30/37) -- zero included -- or one unit when it
     * states none; null when what it states is not a quantity.
     *
     * `productUomId` is the unit the product is stocked in. This base reading
     * ignores it, as barcode_stock's does; it is the seam a module that reads
     * richer barcodes patches, to turn a GS1 net weight into the product's unit.
     */
    // eslint-disable-next-line no-unused-vars
    scannedQuantity(scan, productUomId) {
        const stated = scan?.qty ?? scan?.quantity;
        if (stated === undefined || stated === null || stated === "") {
            return 1;
        }
        const qty = Number(stated);
        return Number.isFinite(qty) && qty >= 0 ? qty : null;
    }

    // --- add a product from the "+" selector ----------------------------------

    addProduct() {
        if (this.state.applying) {
            return;
        }
        this.store.navigate("inventory_product_selector", {
            locationId: this.state.locationId,
            locationName: this.state.locationName,
            lines: this.state.lines.map((l) => ({...l})),
            // Keep out of the "+" picker only the untracked products already
            // listed (those can have a single line). Lot/serial-tracked
            // products stay pickable: the operator legitimately needs several
            // lines for the same product, one per lot/serial number.
            excludeProductIds: [
                ...new Set(
                    this.state.lines
                        .filter((l) => (l.tracking || "none") === "none")
                        .map((l) => l.product_id)
                ),
            ],
        });
    }

    // --- shared add/increment -------------------------------------------------

    /**
     * Add a scanned or picked product and lot to the count, or add to its line.
     *
     * @param {Object} product the product
     * @param {String|null} lotName the lot/serial number read, if any
     * @param {Number|null} qty what a scan counts; null when the product is
     *   picked from the "+" selector, which counts nothing
     */
    async addOrIncrement(product, lotName, qty) {
        const tracking = product.tracking || "none";
        const key = this.lineKey(product.id, lotName);
        const line = this.state.lines.find(
            (l) => this.lineKey(l.product_id, l.lot_name) === key
        );
        if (line) {
            this.countAgain(line, product, lotName, qty);
            return;
        }
        const newLine = {
            _id: ++this._seq,
            product_id: product.id,
            product_name: product.display_name,
            tracking,
            lot_id: false,
            lot_name: lotName || "",
            theoretical_qty: 0,
            checked_qty: 0,
            uom: product.uom_id?.[1] || "",
            lot_fixed: tracking !== "none" && Boolean(lotName),
            lot_options: [],
            counted: qty === null ? null : this.serialAware(tracking, qty),
            isNew: true,
        };
        // Put a freshly scanned/added product at the TOP, where the operator is
        // looking, instead of appending it out of sight at the bottom.
        this.state.lines.unshift(newLine);
        this.flashLine(newLine);
        if (this.needsLotInput(newLine)) {
            await this.loadLotOptions(newLine);
        }
    }

    /**
     * A product and lot already listed is scanned or picked again: add what it
     * stands for to its line -- a serial number only ever counts one unit --
     * and show the operator which line that is.
     *
     * @param {Object} line the line of that product and lot
     * @param {Object} product the product scanned or picked
     * @param {String|null} lotName the lot/serial number read, if any
     * @param {Number|null} qty the quantity the scan stands for; null when
     *   picked from the selector
     */
    countAgain(line, product, lotName, qty) {
        const serial = product.tracking === "serial";
        if (qty !== null && serial && this.isCounted(line)) {
            // A serial number is one unit: reading it again counts nothing.
            this.inventory.notify(this.serialCountedMessage(product, lotName), {
                type: "warning",
            });
        } else if (qty !== null) {
            line.counted = serial
                ? this.serialAware("serial", qty)
                : String((parseFloat(line.counted) || 0) + qty);
        }
        // The line may be far down a long list: flag it so the operator sees
        // what the scan just changed, and bring it into view.
        this.flashLine(line);
    }

    /**
     * The count a scan gives a line: a serial number is one unit, or none.
     *
     * @param {String} tracking the product's tracking
     * @param {Number} qty the quantity scanned
     * @returns {String} the counted quantity
     */
    serialAware(tracking, qty) {
        if (tracking === "serial") {
            return qty > 0 ? "1" : "0";
        }
        return String(qty);
    }

    serialCountedMessage(product, lotName) {
        if (lotName) {
            return _t("Serial number %(lot)s is already counted.", {lot: lotName});
        }
        return _t(
            "%(name)s is already counted: set its serial number before counting another one.",
            {name: product.display_name}
        );
    }

    /**
     * Draw the operator's eye to the line a scan just added or changed: mark it
     * highlighted for a moment and scroll it into view. Purely visual; it never
     * changes the counted data.
     *
     * @param {Object} line the count line to highlight
     */
    flashLine(line) {
        line._flash = true;
        clearTimeout(line._flashTimer);
        line._flashTimer = setTimeout(() => {
            line._flash = false;
        }, 1500);
        // Scroll after the DOM has the (re)ordered line.
        requestAnimationFrame(() => {
            const el = document.getElementById(`inv-count-line-${line._id}`);
            if (el) {
                el.scrollIntoView({behavior: "smooth", block: "nearest"});
            }
        });
    }

    // --- lot handling ---------------------------------------------------------

    /**
     * Suggest the lots the server would take for this line: its company's and
     * the shared ones, so that no suggestion becomes a new lot once applied.
     *
     * @param {Object} line the count line that needs its lot
     * @param {String} [search] what the operator has typed so far
     */
    async loadLotOptions(line, search = "") {
        // They are looked up again as the operator types: only the latest
        // answer may fill the list, whatever order the answers come back in.
        line._lotSearch = (line._lotSearch || 0) + 1;
        const query = line._lotSearch;
        const names = await this.inventory.call(
            "stock.inventory",
            "action_barcode_lot_names",
            [this.state.locationId, line.product_id, search]
        );
        if (query === line._lotSearch) {
            line.lot_options = names;
        }
    }

    // While the count is applied, the lines stay as they were sent.

    setLotName(line, value) {
        if (!this.state.applying) {
            line.lot_name = value;
            this.loadLotOptions(line, value);
        }
    }

    needsLotInput(line) {
        return line.tracking !== "none" && !line.lot_fixed;
    }

    // --- quantities -----------------------------------------------------------

    setCounted(line, value) {
        if (!this.state.applying) {
            line.counted = value === "" ? null : value;
        }
    }

    isCounted(line) {
        return line.counted !== null && line.counted !== "";
    }

    diff(line) {
        if (!this.isCounted(line)) {
            return null;
        }
        return (parseFloat(line.counted) || 0) - line.theoretical_qty;
    }

    /**
     * How a difference reads on the line: its sign, and nothing after the
     * decimal point that is not there (`+2`, `-0.5`, `0`).
     *
     * @param {Number} value the difference between the count and the stock
     * @returns {String} the difference to show
     */
    formatDiff(value) {
        const text = this.formatQty(value);
        return value > 0 ? `+${text}` : text;
    }

    formatQty(value) {
        return formatFloat(value, {trailingZeros: false});
    }

    diffClass(line) {
        const diff = this.diff(line);
        if (diff > 0) {
            return "ilx-inv-diff-up";
        }
        return diff < 0 ? "ilx-inv-diff-down" : "ilx-inv-diff-none";
    }

    removeLine(line) {
        if (this.state.applying) {
            return;
        }
        const index = this.state.lines.indexOf(line);
        if (index !== -1) {
            this.state.lines.splice(index, 1);
        }
    }

    get countedLines() {
        return this.state.lines.filter((l) => this.isCounted(l));
    }

    // --- apply ----------------------------------------------------------------

    /**
     * Apply the counted lines. Should the stock of a counted product have
     * changed since the screen showed it, the server applies nothing and says
     * so: the operator is asked whether to apply anyway, and `confirmed` is
     * the count that answer was about -- it is only forced while the counted
     * lines are still exactly those.
     *
     * @param {Boolean} force apply over the stock changes
     * @param {String} [confirmed] the count the operator confirmed
     */
    async apply(force = false, confirmed = null) {
        if (this.state.applying) {
            return;
        }
        const counted = this.countedLines;
        if (!counted.length) {
            this.inventory.notify(_t("Count at least one product before applying."), {
                type: "warning",
            });
            return;
        }
        const missingLot = counted.find(
            (l) => l.tracking !== "none" && !String(l.lot_name || "").trim()
        );
        if (missingLot) {
            this.inventory.notify(
                _t("Set the lot/serial for %(name)s before applying.", {
                    name: missingLot.product_name,
                }),
                {type: "warning"}
            );
            return;
        }
        const notNumber = counted.find((l) => !Number.isFinite(Number(l.counted)));
        if (notNumber) {
            this.inventory.notify(
                _t("The counted quantity for %(name)s is not a number.", {
                    name: notNumber.product_name,
                }),
                {type: "warning"}
            );
            return;
        }
        const payload = counted.map((l) => ({
            product_id: l.product_id,
            lot_name: l.lot_name || "",
            counted_qty: Number(l.counted),
            theoretical_qty: l.checked_qty ?? l.theoretical_qty,
        }));
        // What the operator counted, without the stock shown next to it: the
        // stock changes the warning is about update that.
        const signature = JSON.stringify(
            payload.map(({product_id, lot_name, counted_qty}) => [
                product_id,
                lot_name,
                counted_qty,
            ])
        );
        this.state.applying = true;
        try {
            const result = await this.inventory.call(
                "stock.inventory",
                "action_barcode_apply_count",
                [this.state.locationId, payload],
                {force: force && confirmed === signature}
            );
            if (!result.done) {
                this.state.applying = false;
                this.showStockChanges(result.changed || [], signature);
                return;
            }
            this.inventory.notify(
                _t("Inventory adjusted: %(n)s product(s).", {n: result.adjusted}),
                {type: "success"}
            );
            this.store.navigate("main", {}, {clearHistory: true});
        } catch {
            // The API wrapper already surfaced the server error to the operator.
            this.state.applying = false;
        }
    }

    /**
     * The stock of some counted products changed since the screen showed it:
     * show the stock as it is now on their lines, and ask whether to apply the
     * count all the same, as the back office does with outdated counts.
     *
     * The count is still checked against the stock shown as counting began
     * (`checked_qty`): only "Apply anyway" applies it over the change, and
     * applying again after cancelling asks again.
     *
     * @param {Object[]} changed the products and lots whose stock changed
     * @param {String} signature the count the question is about
     */
    showStockChanges(changed, signature) {
        for (const change of changed) {
            for (const line of this.state.lines) {
                if (
                    line.product_id === change.product_id &&
                    (line.lot_name || "") === (change.lot_name || "")
                ) {
                    line.theoretical_qty = change.now;
                }
            }
        }
        const rows = changed.map((c) => {
            // Built apart from the _t() call: a template literal among its
            // arguments hides the message from Odoo's translation extractor.
            const what = c.lot_name
                ? c.product_name + " (" + c.lot_name + ")"
                : c.product_name;
            return _t("• %(what)s: %(shown)s %(uom)s when counting, %(now)s now", {
                what,
                shown: this.formatQty(c.shown),
                now: this.formatQty(c.now),
                uom: c.uom,
            });
        });
        this.inventory.openDialog(ConfirmationDialog, {
            title: _t("Stock changed"),
            body: [
                _t("The stock changed here while you counted:"),
                ...rows,
                "",
                _t(
                    "Your counted quantities will be set all the same. Apply the count?"
                ),
            ].join("\n"),
            confirmLabel: _t("Apply anyway"),
            confirm: () => this.apply(true, signature),
            cancel: () => undefined,
        });
    }

    goBack() {
        this.store.goBack();
    }

    static template = "barcode_inventory.InventoryCountScreen";
}

barcodeScreens.add("inventory_count", {component: InventoryCountScreen});
