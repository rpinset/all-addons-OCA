import {
    barcodeMatchAnyDomain,
    barcodeMatchDomain,
} from "@barcode_scanner/js/utils/scan_match.esm";
import {Component, onWillStart, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {roundPrecision} from "@web/core/utils/numbers";
import {useService} from "@web/core/utils/hooks";

// The products the scanner offers for an order: goods that can be purchased.
export const PURCHASABLE_PRODUCTS = [
    ["type", "=", "consu"],
    ["purchase_ok", "=", true],
];

// What a product search reads: enough to draw a line (the order prices it).
export const PRODUCT_FIELDS = [
    "display_name",
    "default_code",
    "tracking",
    "uom_id",
    "uom_po_id",
];

// The units of measure, read once: a label counts pieces in the product's unit,
// while an order line is in its purchase unit.
let uomsById = null;

/**
 * Create a purchase order from the scanner: pick a vendor, a destination
 * location and a buyer, scan or add the products (a GS1 label carries its own
 * lot and piece count), then create the order and -- if asked -- confirm it,
 * which raises the incoming picking. The server does all of it in one call.
 *
 * The selections round-trip through the selector screens: each returns here via
 * navigate("purchase", {...}), so the whole draft lives in the route params
 * while the operator moves between screens.
 */
export class PurchaseScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        const params = this.props.params || {};
        this.state = useState({
            supplier: params.supplier || null,
            destinationLocation: params.destinationLocation || null,
            buyer: params.buyer || null,
            vendorRef: params.vendorRef || "",
            lines: JSON.parse(JSON.stringify(params.lines || [])),
            // On by default: the scanner flow is meant to raise a confirmed
            // order in one go (which generates the incoming picking); untick it
            // to keep the order as a draft RFQ instead.
            autoValidate: params.autoValidate ?? true,
            saving: false,
        });
        onWillStart(async () => {
            await this.loadUoms();
            if (params.addProduct) {
                // Back from the product selector with the product picked there.
                this.addPicked(params.addProduct);
            }
            await this.refreshPrices();
        });

        useBarcodeHandler({
            onScan: async (barcode, parsedData) => {
                await this.onBarcodeScanned(barcode, parsedData);
            },
        });
    }

    /**
     * Whether a scan must wait because the order is on its way to the server:
     * a scan now would show up on it without being so, then vanish with the
     * screen. Checked again after each lookup, which the save may overtake.
     */
    scanMustWait() {
        if (!this.state.saving) {
            return false;
        }
        this.inventory.notify(_t("Wait until the order is saved to scan again."), {
            type: "warning",
        });
        return true;
    }

    async onBarcodeScanned(barcode, parsedData) {
        if (this.scanMustWait()) {
            return;
        }
        // A scanned location barcode sets the destination; anything else is
        // resolved as a product to add to the order.
        const locationDomain = barcodeMatchDomain(barcode);
        const locations = locationDomain
            ? await this.inventory.searchRead(
                  "stock.location",
                  [["usage", "=", "internal"], ...locationDomain],
                  ["display_name"]
              )
            : [];
        if (this.scanMustWait()) {
            return;
        }
        if (locations.length) {
            this.state.destinationLocation = {
                id: locations[0].id,
                display_name: locations[0].display_name,
            };
            this.inventory.notify(
                _t("Destination location selected: %(name)s", {
                    name: locations[0].display_name,
                }),
                {type: "success"}
            );
            return;
        }
        await this.addScannedProduct(barcode, parsedData);
    }

    async addScannedProduct(barcode, parsedData) {
        const candidates = [
            ...(parsedData?.productCodes || []),
            parsedData?.value,
            barcode,
        ];
        const productDomain = barcodeMatchAnyDomain(candidates);
        const products = productDomain
            ? await this.inventory.searchRead(
                  "product.product",
                  [...PURCHASABLE_PRODUCTS, ...productDomain],
                  PRODUCT_FIELDS
              )
            : [];
        if (this.scanMustWait()) {
            return;
        }
        if (!products.length) {
            this.inventory.notify(_t("Product not found."), {type: "warning"});
            return;
        }
        this.addPicked({product: products[0], parsed: parsedData || null});
        await this.refreshPrices();
    }

    async loadUoms() {
        if (!uomsById) {
            const uoms = await this.inventory.searchRead(
                "uom.uom",
                [],
                ["factor", "rounding"]
            );
            uomsById = Object.fromEntries(uoms.map((uom) => [uom.id, uom]));
        }
    }

    /**
     * `qty` in the product's unit, converted into its purchase unit (24 pieces
     * are 2 Dozens), rounded as that unit rounds. As it comes when the units
     * are unknown.
     */
    toPurchaseUnit(qty, product) {
        const from = uomsById?.[product.uom_id?.[0]];
        const to = uomsById?.[product.uom_po_id?.[0]];
        if (!from || !to || from === to) {
            return qty;
        }
        return roundPrecision((qty / from.factor) * to.factor, to.rounding);
    }

    /**
     * Add a product scanned here or picked in the product selector, with the
     * lot and the quantity its barcode states.
     *
     * @param {{product: Object, parsed: (Object|null)}} picked
     */
    addPicked({product, parsed}) {
        const lotName = parsed?.lot || parsed?.serial || null;
        this.addLine(product, lotName, this.scannedQuantity(parsed, product));
    }

    /**
     * How much of the product a scan stands for, in its purchase unit -- the
     * unit the order line is in, shown on the line: the pieces the barcode
     * counts (a GS1 count, AI 30/37, in the product's own unit) converted into
     * it, or else one purchase unit.
     *
     * This is the seam a module that reads richer barcodes patches, to turn a
     * GS1 net weight into the purchase unit.
     */
    scannedQuantity(scan, product) {
        const pieces = parseFloat(scan?.qty ?? scan?.quantity ?? 0);
        return pieces > 0 ? this.toPurchaseUnit(pieces, product) : 1;
    }

    /**
     * One line per product and lot: scanning them again adds to it. A serial
     * number stands for a single unit, so it is listed once.
     */
    addLine(product, lotName, qty) {
        const serial = product.tracking === "serial" && Boolean(lotName);
        const existing = this.state.lines.find(
            (l) => l.product_id === product.id && l.lot_name === lotName
        );
        if (existing && serial) {
            this.inventory.notify(
                _t("Serial number %(lot)s is already on the list.", {lot: lotName}),
                {type: "warning"}
            );
            return;
        }
        if (existing) {
            existing.qty += qty;
            return;
        }
        this.state.lines.push({
            product_id: product.id,
            product_name: product.display_name,
            default_code: product.default_code || null,
            qty: serial ? 1 : qty,
            uom_name: product.uom_po_id?.[1] || "",
            // Empty until the operator types one: the order prices the line
            // from the vendor, in the purchase unit and its own currency. The
            // estimate shows that price meanwhile.
            price_unit: null,
            price_estimate: null,
            lot_name: lotName,
            tracking: product.tracking || "none",
        });
    }

    /** Whether the operator typed a price for the line (0 included). */
    hasTypedPrice(line) {
        return line.price_unit !== null && line.price_unit !== "";
    }

    /** The unit price a line will get: the one typed, or the vendor's. */
    linePrice(line) {
        return this.hasTypedPrice(line) ? line.price_unit : line.price_estimate;
    }

    lineSubtotal(line) {
        return ((parseFloat(line.qty) || 0) * (this.linePrice(line) || 0)).toFixed(2);
    }

    /**
     * Ask the server what the order would price the lines without a typed
     * price at, for the vendor chosen and their quantities. Only the latest
     * answer is kept, whatever order they come back in.
     */
    async refreshPrices() {
        const lines = this.state.lines.filter((line) => !this.hasTypedPrice(line));
        if (!this.state.supplier || !lines.length) {
            return;
        }
        this._pricesSeq = (this._pricesSeq || 0) + 1;
        const query = this._pricesSeq;
        const prices = await this.inventory.call(
            "purchase.order",
            "barcode_purchase_prices",
            [
                this.state.supplier.id,
                lines.map((line) => ({
                    product_id: line.product_id,
                    qty: parseFloat(line.qty) || 1,
                })),
            ]
        );
        if (query !== this._pricesSeq) {
            return;
        }
        lines.forEach((line, index) => {
            line.price_estimate = prices[index] ?? null;
        });
    }

    removeLine(line) {
        this.state.lines = this.state.lines.filter(
            (l) => !(l.product_id === line.product_id && l.lot_name === line.lot_name)
        );
    }

    // --- Navigation to the selector screens (the draft rides along as params) ---

    get _draftParams() {
        return {
            supplier: this.state.supplier,
            destinationLocation: this.state.destinationLocation,
            buyer: this.state.buyer,
            vendorRef: this.state.vendorRef,
            lines: this.state.lines,
            autoValidate: this.state.autoValidate,
        };
    }

    selectSupplier() {
        this.store.navigate("purchase_supplier_selector", {...this._draftParams});
    }

    selectDestinationLocation() {
        this.store.navigate("purchase_location_selector", {...this._draftParams});
    }

    selectBuyer() {
        this.store.navigate("purchase_buyer_selector", {
            returnRoute: "purchase",
            returnParams: {...this._draftParams},
        });
    }

    addProduct() {
        this.store.navigate("purchase_product_selector", {...this._draftParams});
    }

    goBack() {
        this.store.navigate("main");
    }

    // --- Create the order ---

    /** Save the order as a draft, whatever the "validate" box says. */
    async saveDraft() {
        await this.createPurchase(false);
    }

    /**
     * Create the order in one call to the server.
     *
     * @param {Boolean} [confirm] confirm it too; by default, as the "validate
     *     automatically" box says
     */
    async createPurchase(confirm = this.state.autoValidate) {
        if (this.state.saving) {
            return;
        }
        if (!this.state.supplier) {
            this.inventory.notify(_t("Please select a supplier."), {type: "warning"});
            return;
        }
        if (!this.state.lines.length) {
            this.inventory.notify(_t("Please add at least one product."), {
                type: "warning",
            });
            return;
        }
        this.state.saving = true;
        try {
            const result = await this.inventory.call(
                "purchase.order",
                "action_barcode_purchase",
                [
                    this.state.supplier.id,
                    this.state.lines.map((line) => ({
                        product_id: line.product_id,
                        qty: parseFloat(line.qty) || 0,
                        // No price lets the server use the vendor's.
                        price_unit: this.hasTypedPrice(line) ? line.price_unit : null,
                        lot_name: line.lot_name || false,
                    })),
                ],
                {
                    confirm,
                    location_dest_id: this.state.destinationLocation?.id || false,
                    user_id: this.state.buyer?.id || false,
                    partner_ref: this.state.vendorRef || false,
                }
            );
            this.notifyOutcome(result, confirm);
            this.store.navigate("main");
        } catch {
            // The API wrapper already surfaced the server error to the operator,
            // and nothing was written: the whole order is one transaction.
        } finally {
            this.state.saving = false;
        }
    }

    /**
     * Say what actually happened, by order number and by the state the server
     * ended up in. A confirmation does not always confirm: with two-step
     * validation the order lands on "To Approve" and raises no receipt yet
     * (the lots read wait on the order for it).
     *
     * @param {{name: String, state: String, missing_lots: String[], unplaced_lots: String[]}} result
     * @param {Boolean} confirm whether the order was meant to be confirmed
     */
    notifyOutcome({name, state, missing_lots, unplaced_lots}, confirm) {
        if (unplaced_lots?.length) {
            this.inventory.notify(
                _t("Set these lots on the receipt by hand: %(lots)s", {
                    lots: unplaced_lots.join(", "),
                }),
                {type: "warning"}
            );
        }
        if (["purchase", "done"].includes(state)) {
            if (missing_lots?.length) {
                this.inventory.notify(
                    _t(
                        "%(name)s confirmed -- set the lot/serial of %(products)s on the receipt.",
                        {name, products: missing_lots.join(", ")}
                    ),
                    {type: "warning"}
                );
                return;
            }
            this.inventory.notify(_t("Purchase order %(name)s confirmed.", {name}), {
                type: "success",
            });
            return;
        }
        if (state === "to approve") {
            this.inventory.notify(
                _t("Purchase order %(name)s created -- it is waiting for approval.", {
                    name,
                }),
                {type: "warning"}
            );
            return;
        }
        this.inventory.notify(
            confirm
                ? _t("Purchase order %(name)s was created but is still a draft.", {
                      name,
                  })
                : _t("Purchase order %(name)s saved as a draft.", {name}),
            {type: confirm ? "warning" : "success"}
        );
    }

    static template = "barcode_purchase.PurchaseScreen";
}

barcodeScreens.add("purchase", {component: PurchaseScreen});
