import {
    Component,
    onMounted,
    onPatched,
    onWillStart,
    useRef,
    useState,
} from "@odoo/owl";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useService} from "@web/core/utils/hooks";

// Remember the operator's warehouse choice across in-app navigation. The
// module-level variable is the RELIABLE layer: navigation is a client-side
// (SPA) screen swap, so WarehouseOps remounts and re-runs loadData, but this
// variable does NOT reset -- and unlike web storage it can't be blocked by a
// private-mode webview (sessionStorage alone silently failed there). Web
// storage is only a best-effort bonus so the pick also survives a full reload.
const WAREHOUSE_STORAGE_KEY = "barcode.warehouse_ops.selected_id";
let lastSelectedWarehouseId = null;

function readStoredWarehouseId() {
    if (lastSelectedWarehouseId) {
        return lastSelectedWarehouseId;
    }
    try {
        const value = sessionStorage.getItem(WAREHOUSE_STORAGE_KEY);
        return value ? parseInt(value, 10) : null;
    } catch {
        return null;
    }
}

function storeWarehouseId(id) {
    lastSelectedWarehouseId = id || null;
    try {
        if (id) {
            sessionStorage.setItem(WAREHOUSE_STORAGE_KEY, String(id));
        }
    } catch {
        // Web storage blocked: the module-level variable above still carries
        // the pick across in-app navigation for this session.
    }
}

export class WarehouseOps extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this.company = useService("company");
        this.state = useState({
            warehouses: [],
            selectedWarehouseId: null,
        });

        // A <select>'s shown option is driven by its `value` PROPERTY, which OWL
        // may set before the <option> children exist on a fresh mount -- so on
        // returning to this screen the box showed the first option even though
        // state held the remembered warehouse. Re-apply it after every render,
        // once the options are in the DOM.
        this.warehouseSelect = useRef("warehouseSelect");
        onMounted(() => this.syncSelect());
        onPatched(() => this.syncSelect());

        this.openPickings = (type) => {
            const warehouseId = this.state.selectedWarehouseId;
            if (!warehouseId) return;
            this.store.navigate("picking_list", {
                warehouseId: warehouseId,
                type: type,
            });
        };

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        // Only the companies the operator is actually working in (the
        // multi-company switcher selection), not every warehouse configured in
        // the database.
        const allowedCompanyIds = this.company.activeCompanyIds;
        const domain = allowedCompanyIds.length
            ? [["company_id", "in", allowedCompanyIds]]
            : [];
        const warehouses = await this.inventory.searchRead("stock.warehouse", domain, [
            "name",
            "company_id",
        ]);
        const pickingTypes = await this.inventory.searchRead(
            "stock.picking.type",
            [],
            ["warehouse_id", "code"]
        );
        const counts = await this.inventory.readGroup(
            "stock.picking",
            [["state", "not in", ["done", "cancel"]]],
            ["picking_type_id"],
            ["picking_type_id"]
        );
        const countMap = {};
        for (const c of counts) {
            countMap[c.picking_type_id[0]] = c.picking_type_id_count;
        }
        const warehouseMap = {};
        for (const pt of pickingTypes) {
            const warehouseId = pt.warehouse_id?.[0];
            if (!warehouseId) continue;
            if (!warehouseMap[warehouseId]) {
                warehouseMap[warehouseId] = {
                    incoming: 0,
                    internal: 0,
                    outgoing: 0,
                };
            }
            const count = countMap[pt.id] || 0;
            warehouseMap[warehouseId][pt.code] += count;
        }
        this.state.warehouses = warehouses.map((w) => ({
            id: w.id,
            name: w.name,
            companyId: w.company_id?.[0] || null,
            receipts: warehouseMap[w.id]?.incoming || 0,
            internal: warehouseMap[w.id]?.internal || 0,
            delivery: warehouseMap[w.id]?.outgoing || 0,
        }));
        if (this.state.warehouses.length) {
            // Keep the operator's own pick across navigation within the session;
            // only fall back to the active company's warehouse (never just the
            // first, which was rarely theirs) when there is no valid stored one.
            const storedId = readStoredWarehouseId();
            const stored = this.state.warehouses.find((w) => w.id === storedId);
            if (stored) {
                this.state.selectedWarehouseId = stored.id;
            } else {
                const currentCompanyId = this.company.currentCompany?.id;
                const active = this.state.warehouses.find(
                    (w) => w.companyId === currentCompanyId
                );
                this.state.selectedWarehouseId = (
                    active || this.state.warehouses[0]
                ).id;
            }
        }
    }

    get selectedWarehouse() {
        return this.state.warehouses.find(
            (w) => w.id === this.state.selectedWarehouseId
        );
    }

    goBack() {
        this.store.goBack();
    }

    selectWarehouse(ev) {
        this.state.selectedWarehouseId = parseInt(ev.target.value, 10);
        storeWarehouseId(this.state.selectedWarehouseId);
    }

    syncSelect() {
        const el = this.warehouseSelect.el;
        if (
            el &&
            this.state.selectedWarehouseId !== null &&
            this.state.selectedWarehouseId !== undefined
        ) {
            const value = String(this.state.selectedWarehouseId);
            if (el.value !== value) {
                el.value = value;
            }
        }
    }

    static template = "barcode_scanner.WarehouseOps";
}

barcodeScreens.add("warehouse_ops", {component: WarehouseOps});
