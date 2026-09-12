import {Component, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {useService} from "@web/core/utils/hooks";
import {user} from "@web/core/user";
import {imageUrl} from "@web/core/utils/urls";
import {useBarcodeDispatcher} from "@barcode_scanner/js/hooks/use_barcode_dispatcher.esm";
import {barcodeMenuTiles, barcodeScreens} from "@barcode_scanner/js/registries.esm";

export class MainScreen extends Component {
    setup() {
        this.store = useState(useService("barcodeStore"));
        this.avatarState = useState({failed: false});
        useBarcodeDispatcher();
    }

    get menuTiles() {
        return barcodeMenuTiles.getEntries().map(([id, tile]) => ({id, ...tile}));
    }

    onTileClick(tile) {
        tile.action({navigate: this.store.navigate.bind(this.store)});
    }

    get greeting() {
        const tz = user.tz || "UTC";
        const hour = new Intl.DateTimeFormat("en", {
            hour: "numeric",
            hour12: false,
            timeZone: tz,
        }).format(new Date());
        const h = parseInt(hour, 10);
        if (h < 12) return _t("Good morning");
        if (h < 18) return _t("Good afternoon");
        return _t("Good evening");
    }

    get userName() {
        return user.name || "Operational Lead";
    }

    get userInitials() {
        const name = this.userName;
        if (name === "Operational Lead") return "OL";
        const parts = name.split(" ").filter((p) => p.length > 0);
        if (parts.length >= 2) {
            return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
        }
        return name.substring(0, 2).toUpperCase();
    }

    get avatarUrl() {
        const {partnerId, writeDate} = user;
        return imageUrl("res.partner", partnerId, "avatar_128", {unique: writeDate});
    }

    onAvatarError() {
        this.avatarState.failed = true;
    }

    get showAvatarImage() {
        return !this.avatarState.failed;
    }

    goHome() {
        window.location.href = "/web";
    }

    static template = "barcode_scanner.MainScreen";
}

barcodeScreens.add("main", {component: MainScreen});
