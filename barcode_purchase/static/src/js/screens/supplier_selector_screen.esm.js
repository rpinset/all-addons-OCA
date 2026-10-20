import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {Component, onWillStart, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {barcodeMatchDomain} from "@barcode_scanner/js/utils/scan_match.esm";
import {recordImageUrl} from "@barcode_purchase/js/utils/avatar.esm";

// `bin_size` keeps the images themselves off the wire -- see recordImageUrl.
const AVATAR_FIELDS = ["name", "image_128", "city", "country_id", "write_date"];
const AVATAR_OPTIONS = {context: {bin_size: true}};

/**
 * Pick the vendor for a purchase order. Scanning a partner barcode selects it
 * straight away; otherwise the operator taps one from the list. Returns to the
 * purchase screen with the draft params intact.
 */
export class SupplierSelectorScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this.state = useState({
            suppliers: [],
            search: "",
            loading: true,
            selectedSupplier: null,
        });

        useBarcodeHandler({
            onScan: async (barcode) => {
                await this.onBarcodeScanned(barcode);
            },
        });

        onWillStart(async () => {
            await this.loadSuppliers();
        });
    }

    async onBarcodeScanned(barcode) {
        const domain = barcodeMatchDomain(barcode);
        const suppliers = domain
            ? await this.inventory.searchRead(
                  "res.partner",
                  domain,
                  AVATAR_FIELDS,
                  AVATAR_OPTIONS
              )
            : [];
        if (suppliers.length) {
            this.state.selectedSupplier = this._withImage(suppliers[0]);
            this.confirmSelection();
            return;
        }
        this.state.search = barcode;
    }

    _withImage(partner) {
        partner.image_url = recordImageUrl("res.partner", partner);
        return partner;
    }

    async loadSuppliers() {
        const suppliers = await this.inventory.searchRead(
            "res.partner",
            [["supplier_rank", ">", 0]],
            AVATAR_FIELDS,
            AVATAR_OPTIONS
        );
        this.state.suppliers = suppliers.map((s) => this._withImage(s));
        this.state.loading = false;
    }

    get filteredSuppliers() {
        if (!this.state.search) {
            return this.state.suppliers;
        }
        const s = this.state.search.toLowerCase();
        return this.state.suppliers.filter(
            (sup) =>
                sup.name.toLowerCase().includes(s) ||
                (sup.city && sup.city.toLowerCase().includes(s))
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

    selectSupplier(supplier) {
        this.state.selectedSupplier = supplier;
    }

    confirmSelection() {
        if (!this.state.selectedSupplier) {
            return;
        }
        this.store.navigate("purchase", {
            ...this.props.params,
            supplier: {
                id: this.state.selectedSupplier.id,
                name: this.state.selectedSupplier.name,
            },
        });
    }

    goBack() {
        this.store.navigate("purchase", {...this.props.params});
    }

    static template = "barcode_purchase.SupplierSelectorScreen";
}

barcodeScreens.add("purchase_supplier_selector", {
    component: SupplierSelectorScreen,
});
