import {Component, onWillStart, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {barcodeMatchDomain} from "@barcode_scanner/js/utils/scan_match.esm";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useService} from "@web/core/utils/hooks";

export class LocationSelectorScreen extends Component {
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
            onScan: async (barcode, parsedData) => {
                await this.onBarcodeScanned(barcode, parsedData);
            },
        });

        onWillStart(async () => {
            await this.loadLocations();
        });
    }

    async onBarcodeScanned(barcode) {
        const match = barcodeMatchDomain(barcode);
        // Keep a scanned location within the caller's scope too, so scanning a
        // location the operation can't use is rejected just like typing it.
        const scope = this.props.params?.locationDomain || [];
        const domain = match ? [...match, ...scope] : null;
        const locations = domain
            ? await this.inventory.searchRead("stock.location", domain, [
                  "id",
                  "display_name",
                  "usage",
              ])
            : [];
        if (locations.length) {
            this.state.selectedLocation = locations[0];
            this.confirmSelection();
            return;
        }
        // No location carries this barcode: filter the list by it and say so,
        // instead of silently doing nothing.
        this.state.search = barcode;
        this.inventory.notify(_t("No location matches “%(code)s”.", {code: barcode}), {
            type: "warning",
        });
    }

    async loadLocations() {
        // When the caller scopes the picker (e.g. the move wizard restricts the
        // destination to valid locations of the operation, like the back office),
        // honour that domain; otherwise show all internal locations.
        const domain = this.props.params?.locationDomain || [
            ["usage", "=", "internal"],
        ];
        this.state.locations = await this.inventory.searchRead(
            "stock.location",
            domain,
            ["id", "display_name", "usage"]
        );
        this.state.loading = false;
    }

    get filteredLocations() {
        if (!this.state.search) {
            return this.state.locations;
        }
        const search = this.state.search.toLowerCase();
        return this.state.locations.filter((loc) =>
            loc.display_name.toLowerCase().includes(search)
        );
    }

    selectLocation(loc) {
        this.state.selectedLocation = loc;
    }

    confirmSelection() {
        const location = this.state.selectedLocation;
        if (!location) return;

        if (this.props.params.mode === "quick_info_location") {
            this.store.goBack({
                result: location,
                result_type: "location",
            });
            return;
        }

        this.store.goBack({
            ...this.props.params,
            [this.props.params.type]: location,
        });
    }

    updateSearch(ev) {
        this.state.search = ev.target.value;
    }

    goBack() {
        this.store.goBack();
    }
}

LocationSelectorScreen.template = "barcode_scanner.LocationSelectorScreen";

barcodeScreens.add("location_selector", {component: LocationSelectorScreen});
