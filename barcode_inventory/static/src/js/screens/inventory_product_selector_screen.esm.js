import {
    COUNTABLE_PRODUCTS,
    notStorableMessage,
} from "@barcode_inventory/js/screens/inventory_count_screen.esm";
import {Component, onWillStart, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {barcodeMatchDomain} from "@barcode_scanner/js/utils/scan_match.esm";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useService} from "@web/core/utils/hooks";

/**
 * Product selector for the inventory count, opened from the count screen's "+"
 * -- like the back office, so a product not yet in the location can be added by
 * searching (or scanning) it. It carries the count in progress through the
 * navigation params and hands the picked product back to the count screen.
 */
export class InventoryProductSelectorScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this.state = useState({
            search: "",
            results: [],
            loading: true,
        });

        useBarcodeHandler({
            onScan: async (barcode, parsedData) => {
                await this.onBarcodeScanned(barcode, parsedData);
            },
        });

        onWillStart(async () => {
            await this.search();
        });
    }

    async search() {
        // Searches run as the operator types: only the latest one may fill the
        // list, whatever order the answers come back in.
        this._searchSeq = (this._searchSeq || 0) + 1;
        const query = this._searchSeq;
        const term = this.state.search;
        const exclude = this.props.params?.excludeProductIds || [];
        const domain = [...COUNTABLE_PRODUCTS];
        if (term) {
            domain.push("|", ["name", "ilike", term], ["barcode", "ilike", term]);
        }
        if (exclude.length) {
            // Hide the untracked products the count already lists.
            domain.push(["id", "not in", exclude]);
        }
        const results = await this.inventory.searchRead(
            "product.product",
            domain,
            ["id", "display_name", "tracking", "uom_id"],
            {limit: 50}
        );
        if (query !== this._searchSeq) {
            return;
        }
        this.state.results = results;
        this.state.loading = false;
    }

    onSearchInput(ev) {
        this.state.search = ev.target.value;
        this.search();
    }

    async onBarcodeScanned(barcode, parsed) {
        const code = parsed?.gtin || parsed?.value || barcode;
        const domain = barcodeMatchDomain(code);
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
            this.inventory.notify(_t("No product matches “%(code)s”.", {code}), {
                type: "warning",
            });
            return;
        }
        const product = products.find((p) => p.is_storable);
        if (!product) {
            this.inventory.notify(notStorableMessage(products[0]), {type: "warning"});
            return;
        }
        this.pickProduct(product);
    }

    backParams() {
        const params = this.props.params || {};
        return {
            locationId: params.locationId,
            locationName: params.locationName,
            lines: params.lines || [],
        };
    }

    pickProduct(product) {
        this.store.goBack({
            ...this.backParams(),
            addProduct: {
                id: product.id,
                display_name: product.display_name,
                tracking: product.tracking,
                uom_id: product.uom_id,
            },
        });
    }

    goBack() {
        // Return without adding, keeping the count in progress intact.
        this.store.goBack(this.backParams());
    }

    static template = "barcode_inventory.InventoryProductSelectorScreen";
}

barcodeScreens.add("inventory_product_selector", {
    component: InventoryProductSelectorScreen,
});
