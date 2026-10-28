import {onWillStart, useState} from "@odoo/owl";
import {PickingInfoTab} from "@barcode_stock/js/components/picking_info_tab.esm";
import {_t} from "@web/core/l10n/translation";
import {patch} from "@web/core/utils/patch";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";

/**
 * Show the operation's delivery zone in its Information tab and let the
 * operator change it, as the back office's Delivery Zone field does. The
 * change is written at once, like the responsible; `partner_delivery_zone`
 * carries it on to the sale order.
 */
patch(PickingInfoTab.prototype, {
    setup() {
        super.setup(...arguments);
        this.inventory = useBarcodeScanner();
        this.zoneState = useState({
            zones: [],
            zone: false,
            saving: false,
            failed: false,
        });
        onWillStart(() => this.loadDeliveryZone());
    },

    /**
     * Read the zones and the operation's own. Should that fail, the selector
     * stays disabled: without the operation's real zone, a change could
     * overwrite it unseen. The API wrapper has already told the operator.
     */
    async loadDeliveryZone() {
        try {
            await this.readDeliveryZone();
        } catch {
            this.zoneState.failed = true;
        }
    },

    async readDeliveryZone() {
        const pickingId = this.props.picking?.id;
        const [zones, records] = await Promise.all([
            this.inventory.searchRead("partner.delivery.zone", [], ["id", "name"]),
            pickingId
                ? this.inventory.read(
                      "stock.picking",
                      [pickingId],
                      ["delivery_zone_id"]
                  )
                : [],
        ]);
        this.zoneState.zones = zones;
        this.zoneState.zone = records[0]?.delivery_zone_id || false;
    },

    /**
     * The zones to choose from. An archived zone still set on the operation is
     * kept in the list, so the selector shows it instead of "No zone".
     */
    get deliveryZoneOptions() {
        const zones = this.zoneState.zones;
        const current = this.zoneState.zone;
        if (current && !zones.some((zone) => zone.id === current[0])) {
            return [...zones, {id: current[0], name: current[1]}];
        }
        return zones;
    },

    isDeliveryZoneSelected(zone) {
        return this.zoneState.zone?.[0] === zone.id;
    },

    async onDeliveryZoneChange(ev) {
        const pickingId = this.props.picking?.id;
        if (!pickingId) {
            return;
        }
        const zoneId = parseInt(ev.target.value, 10) || false;
        const previous = this.zoneState.zone;
        const zone = this.deliveryZoneOptions.find((z) => z.id === zoneId);
        this.zoneState.zone = zone ? [zone.id, zone.name] : false;
        this.zoneState.saving = true;
        try {
            await this.inventory.write("stock.picking", [pickingId], {
                delivery_zone_id: zoneId,
            });
            this.inventory.notify(_t("Delivery zone updated."), {type: "success"});
        } catch {
            // The API wrapper already surfaced the server error: show the zone
            // the operation still has.
            this.zoneState.zone = previous;
            ev.target.value = previous ? String(previous[0]) : "";
        } finally {
            this.zoneState.saving = false;
        }
    },
});
