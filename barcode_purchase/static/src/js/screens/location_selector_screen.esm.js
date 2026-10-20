import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {Component, onWillStart, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {barcodeMatchDomain} from "@barcode_scanner/js/utils/scan_match.esm";

/**
 * Pick the destination location for a purchase receipt. The candidate list is
 * the destination of each incoming operation type, so the operator only sees
 * places goods actually get received. Scanning a location barcode selects it.
 */
export class PurchaseLocationSelectorScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this.state = useState({
            locations: [],
            search: "",
            loading: true,
            selectedLocation: null,
        });

        useBarcodeHandler({
            onScan: async (barcode) => {
                await this.onBarcodeScanned(barcode);
            },
        });

        onWillStart(async () => {
            await this.loadLocations();
        });
    }

    async onBarcodeScanned(barcode) {
        const domain = barcodeMatchDomain(barcode);
        const locations = domain
            ? await this.inventory.searchRead(
                  "stock.location",
                  [["usage", "=", "internal"], ...domain],
                  ["display_name"]
              )
            : [];
        if (locations.length) {
            this.state.selectedLocation = locations[0];
            this.confirmSelection();
            return;
        }
        this.state.search = barcode;
    }

    async loadLocations() {
        // Only the destinations of incoming operation types -- where a receipt
        // can actually land.
        const pickingTypes = await this.inventory.searchRead(
            "stock.picking.type",
            [["code", "=", "incoming"]],
            ["default_location_dest_id"],
            {order: "id"}
        );
        const locationIds = pickingTypes
            .map((pt) => pt.default_location_dest_id && pt.default_location_dest_id[0])
            .filter((id) => id);
        const domain = locationIds.length
            ? [["id", "in", locationIds]]
            : [["usage", "=", "internal"]];
        this.state.locations = await this.inventory.searchRead(
            "stock.location",
            domain,
            ["display_name", "usage"]
        );
        this.state.loading = false;
    }

    get filteredLocations() {
        if (!this.state.search) {
            return this.state.locations;
        }
        const s = this.state.search.toLowerCase();
        return this.state.locations.filter((loc) =>
            loc.display_name.toLowerCase().includes(s)
        );
    }

    selectLocation(loc) {
        this.state.selectedLocation = loc;
    }

    confirmSelection() {
        const location = this.state.selectedLocation;
        if (!location) {
            return;
        }
        this.store.navigate("purchase", {
            ...this.props.params,
            destinationLocation: {
                id: location.id,
                display_name: location.display_name,
            },
        });
    }

    goBack() {
        this.store.navigate("purchase", {...this.props.params});
    }

    static template = "barcode_purchase.PurchaseLocationSelectorScreen";
}

barcodeScreens.add("purchase_location_selector", {
    component: PurchaseLocationSelectorScreen,
});
