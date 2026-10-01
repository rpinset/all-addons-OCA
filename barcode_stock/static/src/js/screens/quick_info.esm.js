import {Component, onWillStart, useState} from "@odoo/owl";
import {
    barcodeMatchAnyDomain,
    barcodeMatchDomain,
} from "@barcode_scanner/js/utils/scan_match.esm";
import {_t} from "@web/core/l10n/translation";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {parseBarcode} from "@barcode_scanner/js/barcode_parser.esm";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useService} from "@web/core/utils/hooks";

export class QuickInfoScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this.state = useState({
            barcode: "",
            result: null,
            resultType: null,
            resultDetails: null,
            locationStock: [],
            productStock: [],
            stockPage: 0,
            lot: null,
            lotStock: [],
        });
        this.stockPageSize = 15;

        useBarcodeHandler({
            onScan: async (barcode, parsedData) => {
                await this.onBarcodeScanned(barcode, parsedData);
            },
        });

        onWillStart(async () => {
            if (this.props.params && this.props.params.mode) {
                this.state.mode = this.props.params.mode;
            }
            if (this.props.params && this.props.params.result) {
                await this.loadResult(
                    this.props.params.result,
                    this.props.params.result_type
                );
            }
        });
    }

    async loadResult(result, resultType, {lotName = null} = {}) {
        this.state.result = result;
        this.state.resultType = resultType;
        this.state.locationStock = [];
        this.state.productStock = [];
        this.state.stockPage = 0;
        this.state.lot = null;
        this.state.lotStock = [];
        if (resultType === "product") {
            const products = await this.inventory.searchRead(
                "product.product",
                [["id", "=", result.id]],
                [
                    "name",
                    "default_code",
                    "barcode",
                    "standard_price",
                    "list_price",
                    "tracking",
                    "type",
                    "is_storable",
                    "qty_available",
                    "uom_id",
                ]
            );
            this.state.resultDetails = products.length ? products[0] : null;
            if (this.state.resultDetails) {
                // Where this product physically sits: on-hand grouped by
                // internal location -- the mirror of the location->products
                // direction, which was the missing half of the quick lookup.
                const quants = await this.inventory.readGroup(
                    "stock.quant",
                    [
                        ["product_id", "=", result.id],
                        ["location_id.usage", "=", "internal"],
                    ],
                    ["location_id", "quantity"],
                    ["location_id"]
                );
                this.state.productStock = quants
                    .filter((q) => q.quantity > 0)
                    .map((q) => ({
                        locationId: q.location_id[0],
                        locationName: q.location_id[1],
                        quantity: q.quantity,
                    }));
            }
            if (this.state.resultDetails && lotName) {
                await this.loadLot(result.id, lotName);
            }
        } else if (resultType === "location") {
            const locations = await this.inventory.searchRead(
                "stock.location",
                [["id", "=", result.id]],
                ["display_name", "barcode", "usage"]
            );
            this.state.resultDetails = locations.length ? locations[0] : null;
            if (this.state.resultDetails) {
                const quants = await this.inventory.readGroup(
                    "stock.quant",
                    [["location_id", "=", result.id]],
                    ["product_id", "quantity"],
                    ["product_id"]
                );
                this.state.locationStock = quants
                    .filter((q) => q.quantity > 0)
                    .map((q) => ({
                        productId: q.product_id[0],
                        productName: q.product_id[1],
                        quantity: q.quantity,
                    }));
            }
        }
    }

    /**
     * A scan can name a lot or serial on top of the product, so show where that
     * lot actually sits — the question an operator scanning a labelled pallet is
     * really asking.
     */
    async loadLot(productId, lotName) {
        const [lot] = await this.inventory.searchRead(
            "stock.lot",
            [
                ["product_id", "=", productId],
                ["name", "=", lotName],
            ],
            ["name"]
        );
        if (!lot) {
            this.inventory.notify(
                _t("Lot %(lot)s not found for this product.", {lot: lotName}),
                {
                    type: "warning",
                }
            );
            return;
        }
        this.state.lot = lot;
        const quants = await this.inventory.readGroup(
            "stock.quant",
            [["lot_id", "=", lot.id]],
            ["location_id", "quantity"],
            ["location_id"]
        );
        this.state.lotStock = quants
            .filter((quant) => quant.quantity > 0)
            .map((quant) => ({
                locationId: quant.location_id[0],
                locationName: quant.location_id[1],
                quantity: quant.quantity,
            }));
    }

    goBack() {
        if (this.state.resultDetails) {
            this.state.result = null;
            this.state.resultDetails = null;
            this.state.resultType = null;
            this.state.locationStock = [];
            this.state.productStock = [];
            this.state.stockPage = 0;
            this.state.lot = null;
            this.state.lotStock = [];
            return;
        }
        this.store.goBack();
    }

    openProductSelector() {
        this.store.navigate("product_selector", {
            mode: "quick_info_product",
            return_mode: this.state.mode,
        });
    }

    openLocationSelector() {
        this.store.navigate("location_selector", {
            mode: "quick_info_location",
            return_mode: this.state.mode,
        });
    }

    get paginatedStock() {
        const start = this.state.stockPage * this.stockPageSize;
        return this.state.locationStock.slice(start, start + this.stockPageSize);
    }

    get stockTotalPages() {
        return Math.ceil(this.state.locationStock.length / this.stockPageSize);
    }

    nextStockPage() {
        if (this.state.stockPage < this.stockTotalPages - 1) {
            this.state.stockPage++;
        }
    }

    prevStockPage() {
        if (this.state.stockPage > 0) {
            this.state.stockPage--;
        }
    }

    onInputKeydown(ev) {
        if (ev.key === "Enter") {
            this.searchBarcode();
        }
    }

    async searchBarcode() {
        const barcode = this.state.barcode;
        if (!barcode) {
            this.inventory.notify(_t("Enter a barcode."), {type: "warning"});
            return;
        }
        // A typed barcode goes through the same parsers as a scanned one, so a
        // code carrying more than a product reads the same either way.
        await this.lookupAndShow(barcode, parseBarcode(barcode));
    }

    async onBarcodeScanned(barcode, parsedData) {
        if (!(parsedData?.value || barcode)) {
            this.inventory.notify(_t("Barcode not recognized."), {type: "warning"});
            return;
        }
        this.state.barcode = "";
        await this.lookupAndShow(barcode, parsedData);
    }

    async lookupAndShow(barcode, parsedData = null) {
        const lotName = parsedData?.lot || parsedData?.serial || null;
        try {
            // A GS1 GTIN has several equivalent forms; match every candidate so
            // the product is found whichever variant it is stored under.
            const candidates = [
                ...(parsedData?.productCodes || []),
                parsedData?.value,
                barcode,
            ];
            const productDomain = barcodeMatchAnyDomain(candidates);
            const products = productDomain
                ? await this.inventory.searchRead("product.product", productDomain, [
                      "display_name",
                  ])
                : [];
            if (products.length) {
                this.state.barcode = "";
                await this.loadResult(products[0], "product", {lotName});
                return;
            }
            const locationDomain = barcodeMatchDomain(barcode);
            const locations = locationDomain
                ? await this.inventory.searchRead("stock.location", locationDomain, [
                      "display_name",
                  ])
                : [];
            if (locations.length) {
                this.state.barcode = "";
                await this.loadResult(locations[0], "location");
                return;
            }
            this.inventory.notify(_t("Barcode not found."), {type: "danger"});
        } catch (error) {
            console.error(error);
            this.inventory.notify(_t("Search failed."), {type: "danger"});
        }
    }
}

QuickInfoScreen.template = "barcode_scanner.QuickInfoScreen";

barcodeScreens.add("quick_info", {component: QuickInfoScreen});
