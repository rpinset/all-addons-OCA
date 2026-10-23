import {Component, onWillStart, useEffect, useRef, useState} from "@odoo/owl";
import {ConfirmationDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {_t} from "@web/core/l10n/translation";
import {barcodeMatchAnyDomain} from "@barcode_scanner/js/utils/scan_match.esm";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {formatFloat} from "@web/core/utils/numbers";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useService} from "@web/core/utils/hooks";

// What the back office's product field offers on a scrap: goods, never a
// service or a combo, which have no stock to write off.
export const SCRAPPABLE_PRODUCTS = [["type", "=", "consu"]];

/**
 * Scrap lines of one location. The operator scans the goods to write off (a GS1
 * label also brings its lot/serial and piece count), adds others from the "+"
 * product selector, sets each quantity and lot, picks the scrap reasons and
 * scraps. Each line shows how much of it the location holds, and the lot field
 * suggests the lots actually stored there.
 *
 * When a line asks for more than the location holds, the server returns it
 * instead of scrapping, and the operator is asked whether to scrap anyway -- the
 * same choice the back office offers.
 *
 * The lines in progress survive the round-trip to the product selector: they
 * are carried through the navigation params and restored on the way back.
 */
export class ScrapScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this._seq = 0;
        this.state = useState({
            locationId: null,
            locationName: "",
            lines: [],
            stock: [],
            reasons: [],
            reasonIds: [],
            scrapLocationId: null,
            scrapLocations: [],
            // Name being typed for a new scrap reason; null while the field is closed.
            newReason: null,
            loading: true,
            scrapping: false,
        });

        this.newReasonRef = useRef("newReason");
        useEffect(
            (open) => {
                if (open && this.newReasonRef.el) {
                    this.newReasonRef.el.focus();
                }
            },
            () => [this.state.newReason !== null]
        );

        useBarcodeHandler({
            onScan: async (barcode, parsedData) => {
                await this.onBarcodeScanned(barcode, parsedData);
            },
        });

        onWillStart(async () => {
            const params = this.props.params || {};
            this.state.locationId = params.locationId || null;
            this.state.locationName = params.locationName || "";
            this.state.reasonIds = [...(params.reasonIds || [])];
            this.state.scrapLocationId = params.scrapLocationId || null;
            if (Array.isArray(params.lines)) {
                // Coming back from the product selector: restore the lines.
                this.state.lines = params.lines.map((l) => ({...l}));
                this._seq = this.state.lines.reduce(
                    (max, l) => Math.max(max, l._id || 0),
                    0
                );
            }
            await Promise.all([this.loadStock(), this.loadReasons()]);
            this.state.loading = false;
            if (params.addProduct) {
                await this.addOrIncrement(params.addProduct, null, 1);
            }
        });
    }

    async loadStock() {
        if (!this.state.locationId) {
            return;
        }
        const data = await this.inventory.call(
            "stock.scrap",
            "action_barcode_scrap_location_stock",
            [this.state.locationId]
        );
        this.state.stock = data.stock || [];
        this.state.scrapLocations = data.scrap_locations || [];
        // Keep the destination the operator chose; otherwise take the one the
        // back office preselects for this company.
        const known = this.state.scrapLocations.some(
            (loc) => loc.id === this.state.scrapLocationId
        );
        if (!known) {
            this.state.scrapLocationId = data.scrap_location_id || null;
        }
    }

    setScrapLocation(value) {
        this.state.scrapLocationId = parseInt(value, 10) || null;
    }

    async loadReasons() {
        this.state.reasons = await this.inventory.searchRead(
            "stock.scrap.reason.tag",
            [],
            ["id", "name"]
        );
    }

    // --- scanning -------------------------------------------------------------

    async onBarcodeScanned(barcode, parsed) {
        if (this.state.scrapping) {
            // The lines are on their way to the server: a scan now would show
            // up as scrapped without being so, then vanish with the screen.
            this.inventory.notify(_t("Wait until the scrap is done to scan again."), {
                type: "warning",
            });
            return;
        }
        // Match the product the same tolerant, all-candidates way the other
        // screens do: a GS1 GTIN has several equivalent variant forms, and the
        // parser's value can differ from the raw scan.
        const candidates = [
            ...(parsed?.productCodes || []),
            parsed?.gtin,
            parsed?.value,
            barcode,
        ];
        const domain = barcodeMatchAnyDomain(candidates);
        const products = domain
            ? await this.inventory.searchRead(
                  "product.product",
                  [...SCRAPPABLE_PRODUCTS, ...domain],
                  ["id", "display_name", "tracking", "uom_id"]
              )
            : [];
        if (!products.length) {
            this.inventory.notify(
                _t("No product matches “%(code)s”.", {code: parsed?.value || barcode}),
                {type: "warning"}
            );
            return;
        }
        const lotName = parsed?.lot || parsed?.serial || null;
        const qty = this.scannedQuantity(parsed, products[0].uom_id?.[0]);
        await this.addOrIncrement(products[0], lotName, qty);
    }

    /**
     * How much of the product a scan stands for: the piece count the barcode
     * states (a GS1 count, AI 30/37), or one unit.
     *
     * `productUomId` is the unit the product is stocked in. This base reading
     * ignores it, as barcode_stock's does; it is the seam a module that reads
     * richer barcodes patches, to turn a GS1 net weight into the product's unit.
     */
    // eslint-disable-next-line no-unused-vars
    scannedQuantity(scan, productUomId) {
        return parseFloat(scan?.qty ?? scan?.quantity ?? 0) || 1;
    }

    // --- add a product from the "+" selector ----------------------------------

    addProduct() {
        this.store.navigate("scrap_product_selector", {
            locationId: this.state.locationId,
            locationName: this.state.locationName,
            lines: this.state.lines.map((l) => ({...l})),
            reasonIds: [...this.state.reasonIds],
            scrapLocationId: this.state.scrapLocationId,
            // Offer first what the location holds: that is what gets scrapped.
            stockProductIds: [...new Set(this.state.stock.map((s) => s.product_id))],
        });
    }

    // --- lines ----------------------------------------------------------------

    stockLots(productId) {
        return this.state.stock.filter((s) => s.product_id === productId && s.lot_id);
    }

    /**
     * The lot of the location's stock a name stands for: the one with exactly
     * that name (lots that differ only in case are distinct lots), or else the
     * one it names in another case, when it names a single one.
     */
    findStockLot(productId, lotName) {
        const name = String(lotName || "").trim();
        if (!name) {
            return null;
        }
        const lots = this.stockLots(productId);
        const exact = lots.find((s) => s.lot_name === name);
        if (exact) {
            return exact;
        }
        const folded = lots.filter(
            (s) => s.lot_name.toLowerCase() === name.toLowerCase()
        );
        return folded.length === 1 ? folded[0] : null;
    }

    lineKey(productId, lotId, lotName) {
        return `${productId}|${lotId || ""}|${String(lotName || "")}`;
    }

    async addOrIncrement(product, lotName, qty) {
        const tracking = product.tracking || "none";
        let lotId = false;
        let name = lotName || "";
        if (tracking !== "none") {
            const match = this.findStockLot(product.id, name);
            const lots = this.stockLots(product.id);
            if (match) {
                lotId = match.lot_id;
                name = match.lot_name;
            } else if (!name && lots.length === 1) {
                // Only one lot of this product here: it can only be that one.
                lotId = lots[0].lot_id;
                name = lots[0].lot_name;
            }
        }
        const key = this.lineKey(product.id, lotId, name);
        const line = this.state.lines.find(
            (l) => this.lineKey(l.product_id, l.lot_id, l.lot_name) === key
        );
        if (line && tracking !== "serial") {
            line.qty = String((parseFloat(line.qty) || 0) + qty);
            this.flashLine(line);
            return;
        }
        if (line && name) {
            this.inventory.notify(
                _t("Serial number %(lot)s is already on the list.", {lot: name}),
                {type: "warning"}
            );
            this.flashLine(line);
            return;
        }
        const newLine = {
            _id: ++this._seq,
            product_id: product.id,
            product_name: product.display_name,
            tracking,
            uom: product.uom_id?.[1] || "",
            lot_id: lotId,
            lot_name: name,
            qty: String(tracking === "serial" ? 1 : qty),
        };
        // Put a freshly scanned/added product at the TOP, where the operator is
        // looking, instead of appending it out of sight at the bottom.
        this.state.lines.unshift(newLine);
        this.flashLine(newLine);
    }

    /**
     * Draw the operator's eye to the line a scan just added or changed: mark it
     * highlighted for a moment and scroll it into view. Purely visual.
     *
     * @param {Object} line the scrap line to highlight
     */
    flashLine(line) {
        line._flash = true;
        clearTimeout(line._flashTimer);
        line._flashTimer = setTimeout(() => {
            line._flash = false;
        }, 1500);
        requestAnimationFrame(() => {
            const el = document.getElementById(`scrap-line-${line._id}`);
            if (el) {
                el.scrollIntoView({behavior: "smooth", block: "nearest"});
            }
        });
    }

    setLotName(line, value) {
        line.lot_name = value;
        const match = this.findStockLot(line.product_id, value);
        line.lot_id = match ? match.lot_id : false;
    }

    setQty(line, value) {
        line.qty = value;
    }

    available(line) {
        const entries = this.state.stock.filter(
            (s) => s.product_id === line.product_id
        );
        let matching = entries;
        if (line.tracking !== "none") {
            if (!line.lot_id) {
                return null;
            }
            matching = entries.filter((s) => s.lot_id === line.lot_id);
        }
        return matching.reduce((total, s) => total + s.quantity, 0);
    }

    formatQty(value) {
        return formatFloat(value, {trailingZeros: false});
    }

    /**
     * What the lines add up to: the total quantity when they all share one unit
     * of measure (otherwise a total means nothing), and how many products.
     *
     * @param {Object[]} lines the scrap lines
     * @returns {{qty: Number, uom: (string|null), products: Number}}
     */
    summarize(lines) {
        const uoms = new Set(lines.map((l) => l.uom));
        return {
            qty: lines.reduce((total, l) => total + (parseFloat(l.qty) || 0), 0),
            uom: uoms.size === 1 ? [...uoms][0] : null,
            products: new Set(lines.map((l) => l.product_id)).size,
        };
    }

    scrapLabel() {
        if (!this.state.lines.length) {
            return _t("Scrap");
        }
        const summary = this.summarize(this.state.lines);
        if (summary.uom === null) {
            return _t("Scrap %(n)s products", {n: summary.products});
        }
        return _t("Scrap %(qty)s %(uom)s", {
            qty: this.formatQty(summary.qty),
            uom: summary.uom,
        });
    }

    scrappedMessage(lines) {
        const summary = this.summarize(lines);
        if (summary.products === 1) {
            return _t("Scrapped %(qty)s %(uom)s of %(name)s.", {
                qty: this.formatQty(summary.qty),
                uom: summary.uom,
                name: lines[0].product_name,
            });
        }
        return _t("Scrapped %(n)s products.", {n: summary.products});
    }

    removeLine(line) {
        const index = this.state.lines.indexOf(line);
        if (index !== -1) {
            this.state.lines.splice(index, 1);
        }
    }

    // --- reasons --------------------------------------------------------------

    isReasonSelected(reason) {
        return this.state.reasonIds.includes(reason.id);
    }

    toggleReason(reason) {
        const index = this.state.reasonIds.indexOf(reason.id);
        if (index === -1) {
            this.state.reasonIds.push(reason.id);
        } else {
            this.state.reasonIds.splice(index, 1);
        }
    }

    startNewReason() {
        this.state.newReason = "";
    }

    cancelNewReason() {
        this.state.newReason = null;
    }

    setNewReason(value) {
        this.state.newReason = value;
    }

    onNewReasonKeydown(ev) {
        if (ev.key === "Enter") {
            ev.preventDefault();
            this.saveNewReason();
        } else if (ev.key === "Escape") {
            this.cancelNewReason();
        }
    }

    /**
     * Create a scrap reason from its typed name, like the back office's reason
     * field quick-creates one, and select it. An existing reason with the same
     * name comes back instead of a duplicate.
     */
    async saveNewReason() {
        const name = String(this.state.newReason || "").trim();
        if (!name) {
            this.cancelNewReason();
            return;
        }
        try {
            const reason = await this.inventory.call(
                "stock.scrap",
                "action_barcode_scrap_create_reason",
                [name]
            );
            if (!this.state.reasons.some((r) => r.id === reason.id)) {
                this.state.reasons.push(reason);
            }
            if (!this.state.reasonIds.includes(reason.id)) {
                this.state.reasonIds.push(reason.id);
            }
            this.state.newReason = null;
        } catch {
            // The API wrapper already surfaced the server error to the operator.
        }
    }

    // --- scrap ----------------------------------------------------------------

    /** Whether the Scrap button can be used: lines, a destination, no scrap running. */
    get canScrap() {
        return (
            !this.state.scrapping &&
            this.state.lines.length > 0 &&
            Boolean(this.state.scrapLocationId)
        );
    }

    /**
     * Scrap the lines. `confirmed` is the payload the operator agreed to scrap
     * anyway after the not-enough-stock warning: the scrap is only forced when
     * the lines are still exactly those, otherwise they are checked again.
     *
     * @param {Boolean} force scrap even what the location does not hold
     * @param {String} [confirmed] the payload the warning was about
     */
    async scrap(force = false, confirmed = null) {
        const lines = this.state.lines;
        if (!lines.length) {
            this.inventory.notify(_t("Scan at least one product to scrap."), {
                type: "warning",
            });
            return;
        }
        const missingLot = lines.find(
            (l) => l.tracking !== "none" && !l.lot_id && !String(l.lot_name).trim()
        );
        if (missingLot) {
            this.inventory.notify(
                _t("Set the lot/serial for %(name)s before scrapping.", {
                    name: missingLot.product_name,
                }),
                {type: "warning"}
            );
            return;
        }
        const noQty = lines.find((l) => !(parseFloat(l.qty) > 0));
        if (noQty) {
            this.inventory.notify(
                _t("Set the quantity to scrap for %(name)s.", {
                    name: noQty.product_name,
                }),
                {type: "warning"}
            );
            return;
        }
        if (!this.state.scrapLocationId) {
            this.inventory.notify(_t("Choose where the scrapped goods go."), {
                type: "warning",
            });
            return;
        }
        const sent = lines.map((l) => ({...l}));
        const payload = sent.map((l) => ({
            product_id: l.product_id,
            lot_id: l.lot_id || false,
            lot_name: l.lot_name || "",
            qty: parseFloat(l.qty) || 0,
        }));
        const signature = JSON.stringify(payload);
        this.state.scrapping = true;
        try {
            const result = await this.inventory.call(
                "stock.scrap",
                "action_barcode_scrap",
                [this.state.locationId, payload, this.state.reasonIds],
                {
                    force: force && confirmed === signature,
                    scrap_location_id: this.state.scrapLocationId,
                }
            );
            if (!result.done) {
                this.state.scrapping = false;
                this.confirmInsufficient(result.insufficient || [], signature);
                return;
            }
            this.inventory.notify(this.scrappedMessage(sent), {type: "success"});
            this.store.navigate("main", {}, {clearHistory: true});
        } catch {
            // The API wrapper already surfaced the server error to the operator.
            this.state.scrapping = false;
        }
    }

    confirmInsufficient(insufficient, signature) {
        const rows = insufficient.map((s) => {
            // Built apart from the _t() call: a template literal among its
            // arguments hides the message from Odoo's translation extractor.
            const what = s.lot_name
                ? s.product_name + " (" + s.lot_name + ")"
                : s.product_name;
            return _t(
                "• %(what)s: %(requested)s %(uom)s to scrap, %(available)s here (stock will be %(remaining)s)",
                {
                    what,
                    requested: this.formatQty(s.requested),
                    available: this.formatQty(s.available),
                    remaining: this.formatQty(s.available - s.requested),
                    uom: s.uom,
                }
            );
        });
        // Say plainly what confirming does: the whole quantity is scrapped (as
        // in the back office), not only what the location holds.
        this.inventory.openDialog(ConfirmationDialog, {
            title: _t("Not enough stock"),
            body: [
                _t("This location does not hold enough stock for:"),
                ...rows,
                "",
                _t("The full quantity will be scrapped. Scrap anyway?"),
            ].join("\n"),
            confirmLabel: _t("Scrap anyway"),
            confirm: () => this.scrap(true, signature),
            cancel: () => undefined,
        });
    }

    goBack() {
        this.store.goBack();
    }

    static template = "barcode_scrap.ScrapScreen";
}

barcodeScreens.add("scrap", {component: ScrapScreen});
