import {Component, onWillStart, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {barcodeMatchDomain} from "@barcode_scanner/js/utils/scan_match.esm";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {recordImageUrl} from "@barcode_stock/js/utils/avatar.esm";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useService} from "@web/core/utils/hooks";

export class ProductSelectorScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this.state = useState({
            products: [],
            search: "",
            loading: true,
            selectedProduct: null,
            qty: 1,
        });

        useBarcodeHandler({
            onScan: async (barcode, parsedData) => {
                await this.onBarcodeScanned(barcode, parsedData);
            },
        });

        onWillStart(async () => {
            await this.loadProducts();
        });
    }

    async onBarcodeScanned(barcode, parsedData) {
        const searchCode = parsedData?.value || barcode;
        const domain = barcodeMatchDomain(searchCode);
        // No image here: the scanned product goes straight to confirmSelection,
        // nothing renders it, and it would cost a full base64 image.
        const products = domain
            ? await this.inventory.searchRead("product.product", domain, [
                  "name",
                  "standard_price",
                  "tracking",
                  "default_code",
                  "type",
              ])
            : [];
        if (products.length) {
            this.state.selectedProduct = products[0];
            this.confirmSelection();
            return;
        }
        // No product carries this barcode: filter the list by it and say so,
        // instead of silently doing nothing.
        this.state.search = searchCode;
        this.inventory.notify(
            _t("No product matches “%(code)s”.", {code: searchCode}),
            {type: "warning"}
        );
    }

    /**
     * Should the image fail anyway -- no session, no network, a filestore that
     * lost the file -- fall back to the initial rather than leave a broken
     * image in the list.
     */
    onImageError(record) {
        record.image_url = false;
    }

    async loadProducts() {
        const domain = [["type", "=", "consu"]];
        // `bin_size` keeps the images themselves off the wire -- see
        // recordImageUrl.
        let products = await this.inventory.searchRead(
            "product.product",
            domain,
            [
                "name",
                "image_128",
                "standard_price",
                "tracking",
                "default_code",
                "type",
                "write_date",
            ],
            {context: {bin_size: true}}
        );

        products = products.map((prod) => {
            prod.image_url = recordImageUrl("product.product", prod);
            return prod;
        });

        this.state.products = products;
        this.state.loading = false;
    }

    get filteredProducts() {
        if (!this.state.search) {
            return this.state.products;
        }
        const search = this.state.search.toLowerCase();
        return this.state.products.filter(
            (p) =>
                p.name.toLowerCase().includes(search) ||
                (p.default_code && p.default_code.toLowerCase().includes(search))
        );
    }

    selectProduct(product) {
        this.state.selectedProduct = product;
    }

    incrementQty() {
        this.state.qty = (parseInt(this.state.qty, 10) || 0) + 1;
    }

    decrementQty() {
        const current = parseInt(this.state.qty, 10) || 1;
        if (current > 1) {
            this.state.qty = current - 1;
        }
    }

    onQtyInput(ev) {
        const val = parseInt(ev.target.value, 10);
        this.state.qty = isNaN(val) || val < 1 ? 1 : val;
    }

    async confirmSelection() {
        const product = this.state.selectedProduct;
        if (!product) return;

        if (this.props.params.mode === "quick_info_product") {
            this.store.goBack({
                result: product,
                result_type: "product",
            });
            return;
        }

        const qty = parseInt(this.state.qty, 10) || 1;
        const lines = this.props.params.lines || [];
        const existing = lines.find((l) => l.product_id === product.id);
        const lots = await this.inventory.searchRead(
            "stock.lot",
            [["product_id", "=", product.id]],
            ["id", "name"]
        );
        if (existing) {
            existing.qty += qty;
        } else {
            lines.push({
                product_id: product.id,
                product_name: product.name,
                qty: qty,
                price_unit: product.standard_price || 0,
                tracking: product.tracking || "none",
                lot_id: null,
                lots: lots,
                default_code: product.default_code || "",
            });
        }
        this.store.goBack({
            ...this.props.params,
            lines: lines,
        });
    }

    updateSearch(ev) {
        this.state.search = ev.target.value;
    }

    goBack() {
        this.store.goBack();
    }
}

ProductSelectorScreen.template = "barcode_scanner.ProductSelectorScreen";

barcodeScreens.add("product_selector", {component: ProductSelectorScreen});
