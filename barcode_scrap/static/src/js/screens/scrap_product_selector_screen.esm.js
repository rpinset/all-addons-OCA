import {Component, onWillStart, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {barcodeMatchDomain} from "@barcode_scanner/js/utils/scan_match.esm";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {SCRAPPABLE_PRODUCTS} from "@barcode_scrap/js/screens/scrap_screen.esm";
import {useService} from "@web/core/utils/hooks";

/**
 * Product selector for a scrap, opened from the scrap screen's "+". With no
 * search it lists what the location holds -- what normally gets scrapped --
 * and a search (or a scan) reaches any product. It carries the lines in
 * progress through the navigation params and hands the picked product back.
 */
export class ScrapProductSelectorScreen extends Component {
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
        let domain = [];
        if (term) {
            domain = ["|", ["name", "ilike", term], ["barcode", "ilike", term]];
        } else {
            domain = [["id", "in", this.props.params?.stockProductIds || []]];
        }
        const results = await this.inventory.searchRead(
            "product.product",
            [...SCRAPPABLE_PRODUCTS, ...domain],
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
            ? await this.inventory.searchRead(
                  "product.product",
                  [...SCRAPPABLE_PRODUCTS, ...domain],
                  ["id", "display_name", "tracking", "uom_id"]
              )
            : [];
        if (!products.length) {
            this.inventory.notify(_t("No product matches “%(code)s”.", {code}), {
                type: "warning",
            });
            return;
        }
        this.pickProduct(products[0]);
    }

    backParams() {
        const params = this.props.params || {};
        return {
            locationId: params.locationId,
            locationName: params.locationName,
            lines: params.lines || [],
            reasonIds: params.reasonIds || [],
            scrapLocationId: params.scrapLocationId || null,
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
        // Return without adding, keeping the lines in progress intact.
        this.store.goBack(this.backParams());
    }

    static template = "barcode_scrap.ScrapProductSelectorScreen";
}

barcodeScreens.add("scrap_product_selector", {
    component: ScrapProductSelectorScreen,
});
