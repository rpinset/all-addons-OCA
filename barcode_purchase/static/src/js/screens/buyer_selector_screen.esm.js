import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {Component, onWillStart, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {recordImageUrl} from "@barcode_purchase/js/utils/avatar.esm";

/**
 * Pick the buyer for a purchase order -- Odoo's native `user_id` on
 * purchase.order, a res.users. The caller passes `returnRoute` and
 * `returnParams`; on confirm/cancel we navigate back there with the selected
 * buyer merged in.
 */
export class BuyerSelectorScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this.state = useState({
            users: [],
            search: "",
            loading: true,
            selectedUser: null,
        });

        useBarcodeHandler({
            onScan: async (barcode) => {
                await this.onBarcodeScanned(barcode);
            },
        });

        onWillStart(async () => {
            await this.loadUsers();
        });
    }

    get _returnRoute() {
        return this.props.params?.returnRoute || "purchase";
    }

    get _returnParams() {
        return {...(this.props.params?.returnParams || {})};
    }

    async onBarcodeScanned(barcode) {
        // A user carries no barcode by default; fall back to filtering the list.
        this.state.search = barcode;
    }

    async loadUsers() {
        // `bin_size` keeps the images themselves off the wire -- see
        // recordImageUrl.
        const users = await this.inventory.searchRead(
            "res.users",
            [["share", "=", false]],
            ["name", "login", "image_128", "write_date"],
            {context: {bin_size: true}}
        );
        this.state.users = users.map((u) => {
            u.image_url = recordImageUrl("res.users", u);
            return u;
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

    get filteredUsers() {
        if (!this.state.search) {
            return this.state.users;
        }
        const s = this.state.search.toLowerCase();
        return this.state.users.filter(
            (u) =>
                u.name.toLowerCase().includes(s) ||
                (u.login && u.login.toLowerCase().includes(s))
        );
    }

    selectUser(user) {
        this.state.selectedUser = user;
    }

    confirmSelection() {
        const user = this.state.selectedUser;
        if (!user) {
            return;
        }
        this.store.navigate(
            this._returnRoute,
            {
                ...this._returnParams,
                buyer: {id: user.id, name: user.name},
            },
            {replace: true}
        );
    }

    goBack() {
        this.store.navigate(
            this._returnRoute,
            {...this._returnParams},
            {
                replace: true,
            }
        );
    }

    static template = "barcode_purchase.BuyerSelectorScreen";
}

barcodeScreens.add("purchase_buyer_selector", {
    component: BuyerSelectorScreen,
});
