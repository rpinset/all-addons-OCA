import {
    PRODUCT_FIELDS,
    PURCHASABLE_PRODUCTS,
} from "@barcode_purchase/js/screens/purchase_screen.esm";
import {Component, onWillStart, useState} from "@odoo/owl";
import {barcodeMatchAnyDomain} from "@barcode_scanner/js/utils/scan_match.esm";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {recordImageUrl} from "@barcode_purchase/js/utils/avatar.esm";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useService} from "@web/core/utils/hooks";

/**
 * Pick a product to add to the purchase order. Scanning a product barcode adds
 * it straight away (carrying the GS1 lot/quantity when present); otherwise the
 * operator taps one from the list. Returns to the purchase screen with the
 * updated draft lines.
 */
export class PurchaseProductSelectorScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this.state = useState({
            products: [],
            search: "",
            loading: true,
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
        const candidates = [
            ...(parsedData?.productCodes || []),
            parsedData?.value,
            barcode,
        ];
        const domain = barcodeMatchAnyDomain(candidates);
        const products = domain
            ? await this.inventory.searchRead(
                  "product.product",
                  [...PURCHASABLE_PRODUCTS, ...domain],
                  PRODUCT_FIELDS
              )
            : [];
        if (products.length) {
            this.confirmSelection(products[0], parsedData || null);
            return;
        }
        this.state.search = parsedData?.value || barcode;
    }

    async loadProducts() {
        // Odoo 18: purchasable goods are type "consu".
        // `bin_size` keeps the images themselves off the wire -- see
        // recordImageUrl.
        this.state.products = await this.inventory.searchRead(
            "product.product",
            PURCHASABLE_PRODUCTS,
            [...PRODUCT_FIELDS, "image_128", "write_date"],
            {context: {bin_size: true}}
        );
        this.state.products = this.state.products.map((p) => {
            p.image_url = recordImageUrl("product.product", p);
            return p;
        });
        this.state.loading = false;
    }

    /**
     * Should the image fail anyway -- no session, no network, a filestore that
     * lost the file -- fall back to the initial rather than leave a broken
     * image in the list.
     */
    onImageError(record) {
        record.image_url = false;
    }

    get filteredProducts() {
        if (!this.state.search) {
            return this.state.products;
        }
        const s = this.state.search.toLowerCase();
        return this.state.products.filter(
            (p) =>
                p.display_name.toLowerCase().includes(s) ||
                (p.default_code && p.default_code.toLowerCase().includes(s))
        );
    }

    /**
     * Hand the picked product back to the purchase screen, which adds it to the
     * lines (with the lot and quantity of its barcode, when it was scanned).
     *
     * @param {Object} product the product picked
     * @param {Object} [parsed] the parsed barcode it was scanned with
     */
    confirmSelection(product, parsed = null) {
        this.store.navigate("purchase", {
            ...this.props.params,
            addProduct: {
                // Only the fields a line needs ride along.
                product: Object.fromEntries(
                    ["id", ...PRODUCT_FIELDS].map((field) => [field, product[field]])
                ),
                parsed,
            },
        });
    }

    goBack() {
        this.store.navigate("purchase", {...this.props.params});
    }

    static template = "barcode_purchase.PurchaseProductSelectorScreen";
}

barcodeScreens.add("purchase_product_selector", {
    component: PurchaseProductSelectorScreen,
});
