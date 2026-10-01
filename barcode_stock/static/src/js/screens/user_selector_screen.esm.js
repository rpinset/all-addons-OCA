import {Component, onWillStart, useState} from "@odoo/owl";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {recordImageUrl} from "@barcode_stock/js/utils/avatar.esm";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useService} from "@web/core/utils/hooks";

const DEFAULT_RETURN_ROUTE = "internal_transfer";

export class UserSelectorScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this.state = useState({
            users: [],
            search: "",
            loading: true,
            selectedUser: this.props.params?.responsible || null,
        });

        useBarcodeHandler({
            onScan: (barcode) => {
                this.state.search = barcode;
            },
        });

        onWillStart(async () => {
            await this.loadUsers();
        });
    }

    get _returnRoute() {
        return this.props.params?.returnRoute || DEFAULT_RETURN_ROUTE;
    }

    get _returnParams() {
        return {...(this.props.params?.returnParams || {})};
    }

    /**
     * Should the image fail anyway -- no session, no network, a filestore that
     * lost the file -- fall back to the initial rather than leave a broken
     * image in the list.
     */
    onImageError(record) {
        record.image_url = false;
    }

    async loadUsers() {
        // `bin_size` keeps the images themselves off the wire -- see
        // recordImageUrl.
        let users = await this.inventory.searchRead(
            "res.users",
            [["share", "=", false]],
            ["name", "login", "image_128", "write_date"],
            {context: {bin_size: true}}
        );

        users = users.map((user) => {
            user.image_url = recordImageUrl("res.users", user);
            return user;
        });

        this.state.users = users;
        this.state.loading = false;
    }

    get filteredUsers() {
        if (!this.state.search) {
            return this.state.users;
        }
        const s = this.state.search.toLowerCase();
        return this.state.users.filter(
            (user) =>
                user.name.toLowerCase().includes(s) ||
                (user.login && user.login.toLowerCase().includes(s))
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
        this.store.goBack({
            ...this._returnParams,
            responsible: {id: user.id, name: user.name},
        });
    }

    goBack() {
        // Leaving without a selection still has to restore what the caller
        // was doing -- its tab, its in-progress lines -- and `goBack`
        // replaces the params rather than merging them, so hand back the
        // ones we were given instead of the staler history entry.
        const returnParams = this.props.params?.returnParams;
        this.store.goBack(returnParams ? {...returnParams} : undefined);
    }
}

UserSelectorScreen.template = "barcode_scanner.UserSelectorScreen";

barcodeScreens.add("user_selector", {component: UserSelectorScreen});
