import {Component, onMounted, onWillStart, onWillUnmount, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useService} from "@web/core/utils/hooks";
import {user} from "@web/core/user";

function lineLotId(line) {
    return line.lot_id?.[0] || false;
}

export class MoveWizardScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this.barcodeScannerState = useService("barcodeScannerState");
        this.barcodeScannerSync = useService("barcodeScannerSync");
        this.feedback = useService("barcodeScannerFeedback");
        this.onLotChange = this.onLotChange.bind(this);
        this.setMode = this.setMode.bind(this);
        this.confirmPick = this.confirmPick.bind(this);
        this.goBack = this.goBack.bind(this);
        this.adjustQty = this.adjustQty.bind(this);
        this.setQty = this.setQty.bind(this);
        this.fulfillRemaining = this.fulfillRemaining.bind(this);
        this.onKeyDown = this.onKeyDown.bind(this);
        this.selectSourceLocation = this.selectSourceLocation.bind(this);
        this.selectDestLocation = this.selectDestLocation.bind(this);

        this.state = useState({
            move: null,
            moveLines: [],
            selectedLotId: this.props.params?.defaultLot
                ? String(this.props.params.defaultLot)
                : null,
            qtyPicked: this.props.params?.defaultQty || 1,
            loading: true,
            tracking: "none",
            mode:
                this.props.params?.createLot && this.isIncoming ? "create_lot" : "pick",
            newLotName: this.props.params?.lotName || "",
            newLotExpirationDate: this.props.params?.expiration || "",
            lots: [],
            useExistingLots: true,
            useCreateLots: true,
            // The source/destination the operator chose, carried across the
            // location-picker round-trip via params (the wizard remounts on
            // return). None chosen, the line keeps its own.
            sourceLocation: this.props.params?.moveSourceLocation || null,
            destLocation: this.props.params?.moveDestLocation || null,
            // Where a lot the reservation does not carry lies, looked up, and
            // whether it lies nowhere under the move's source.
            lotLocation: null,
            lotMissing: false,
        });

        useBarcodeHandler({
            onScan: async (barcode, parsedData) => {
                await this.onBarcodeScanned(barcode, parsedData);
            },
        });

        onWillStart(async () => {
            await this.loadData();
        });

        onMounted(() => {
            document.addEventListener("keydown", this.onKeyDown);
        });

        onWillUnmount(() => {
            document.removeEventListener("keydown", this.onKeyDown);
        });
    }

    async onBarcodeScanned(barcode, parsedData) {
        const normalized = this.barcodeScannerState.applyScanResult({
            barcode,
            ...(parsedData || {}),
        });
        if (!normalized.product) {
            return;
        }
        const product = this.barcodeScannerState.getProductByBarcode(
            normalized.product
        );
        if (!product) {
            this.inventory.notify(
                _t("Scanned barcode is not a product of this operation."),
                {type: "warning"}
            );
            return;
        }
        if (product.id !== this.state.move?.product_id?.[0]) {
            this.onProductScanned(product);
            return;
        }
        await this.applyScannedLot(normalized);
        this.adjustQty(normalized.quantity);
        this.feedback.success();
    }

    /**
     * Apply the lot or serial a scan carries: select it when it already exists,
     * otherwise prefill the create-lot form where creating one is allowed.
     */
    async applyScannedLot({lot, lotName, expiration}) {
        const name = lot?.name || lotName;
        if (!name || !this.isTracked) {
            return;
        }
        if (lot && this.canUseExistingLot) {
            if (!this.state.lots.some((item) => item.id === lot.id)) {
                this.state.lots = [lot, ...this.state.lots];
            }
            this.state.selectedLotId = String(lot.id);
            await this.locateLot();
            return;
        }
        if (!this.canCreateLot) {
            this.inventory.notify(
                _t("Lot %(lot)s is not available for this product.", {lot: name}),
                {type: "warning"}
            );
            return;
        }
        this.state.newLotName = name;
        if (expiration) {
            this.state.newLotExpirationDate = expiration;
        }
        this.setMode("create_lot");
    }

    get isIncoming() {
        return this.props.params?.pickingTypeCode === "incoming";
    }

    /**
     * Open a move reserved against a lot with that lot chosen, as Odoo's own
     * barcode app does: the reservation already says which lot goes. A lot the
     * scan carried, or the operator chose, still wins.
     *
     * @param {Object[]} moveLines the move's lines
     * @param {Object[]} lots the lots offered
     * @returns {Object[]} the lots offered, the reserved one among them
     */
    preselectReservedLot(moveLines, lots) {
        const reservedLotId = this.reservedLine(moveLines)?.lot_id[0];
        if (this.selectedLotIdNumber || !reservedLotId) {
            return lots;
        }
        this.state.selectedLotId = String(reservedLotId);
        const reservedLot = this.barcodeScannerState.lotsById[reservedLotId];
        if (reservedLot && !lots.some((lot) => lot.id === reservedLotId)) {
            return [reservedLot, ...lots];
        }
        return lots;
    }

    /**
     * The reserved line the move goes on with: its first line reserved against
     * a lot that still has something to pick, of a lot not covered yet.
     *
     * @param {Object[]} moveLines the move's lines
     * @returns {Object|null} the line, if any
     */
    reservedLine(moveLines) {
        if (!this.isTracked || !this.followsReservation) {
            return null;
        }
        return (
            moveLines.find(
                (line) =>
                    line.lot_id?.[0] &&
                    this.lineLeft(line) > 0 &&
                    this.reservedLeft(moveLines, line.lot_id[0]) > 0
            ) || null
        );
    }

    /**
     * The reserved line a confirmation goes on: the first line of the lot
     * chosen (of the move, for a product without lots) that still has
     * something to pick, while that lot is not covered. A move reserved over
     * several lines is so picked line by line, each where Odoo reserved it.
     *
     * @returns {Object|null} the line, if any
     */
    get targetLine() {
        const lotId = this.isTracked ? this.selectedLotIdNumber : false;
        const lines = this.state.moveLines || [];
        if (
            !this.followsReservation ||
            (this.isTracked && !lotId) ||
            this.reservedLeft(lines, lotId) <= 0
        ) {
            return null;
        }
        return (
            lines.find(
                (line) => lineLotId(line) === lotId && this.lineLeft(line) > 0
            ) || null
        );
    }

    /**
     * Whether the move is picked line by line as reserved: outside receptions,
     * where Odoo reserves the stock where it lies, unless a tracked product's
     * operation does not pick from existing lots.
     *
     * @returns {Boolean}
     */
    get followsReservation() {
        return !this.isIncoming && (!this.isTracked || this.state.useExistingLots);
    }

    /**
     * Opened without a quantity (tapped, not scanned), the pick starts at no
     * more than what the reserved line worked on still holds.
     */
    fitStartToLine() {
        const left = this.pickableQty;
        if (!this.props.params?.defaultQty && this.targetLine && left > 0) {
            this.state.qtyPicked = Math.min(this.state.qtyPicked, left);
        }
    }

    /**
     * Where the pick comes from, as shown: the location the operator chose,
     * otherwise where a lot the reservation does not carry lies, otherwise that
     * of the line it goes on.
     *
     * @returns {Object|null} the location, as id and display_name
     */
    get shownSourceLocation() {
        return (
            this.state.sourceLocation ||
            this.state.lotLocation ||
            this.lineLocation("location_id")
        );
    }

    /**
     * The source to write on the line: the one the operator chose. Otherwise
     * none, and the line keeps where Odoo reserved its stock.
     *
     * @returns {Number|false} the location's id
     */
    get sourceLocationId() {
        return this.state.sourceLocation?.id || false;
    }

    /**
     * Whether the lot chosen is one the move's reservation does not carry:
     * Odoo reserves it then, where it lies (see pickUnreservedLot).
     *
     * @returns {Boolean}
     */
    get unreservedLot() {
        const lotId = this.selectedLotIdNumber;
        return Boolean(
            lotId &&
                this.isTracked &&
                this.followsReservation &&
                this.state.mode === "pick" &&
                !(this.state.moveLines || []).some((line) => lineLotId(line) === lotId)
        );
    }

    /**
     * Have Odoo pick a lot the reservation does not carry: it takes it from its
     * own quants under the move's source (or the one the operator chose), one
     * line per shelf, package and owner it lies in, marked picked and sent to
     * the destination the operator chose. What the wizard staged so far is
     * sent first.
     *
     * @returns {Promise<Boolean>} whether it was picked
     */
    async pickUnreservedLot() {
        await this.barcodeScannerSync.flush();
        try {
            await this.inventory.call("stock.move", "barcode_pick_lot", [
                [this.moveId],
                this.selectedLotIdNumber,
                this.state.qtyPicked,
                this.sourceLocationId,
                this.state.destLocation?.id || false,
            ]);
        } catch {
            // The API wrapper already told the operator why.
            return false;
        }
        return true;
    }

    /**
     * A lot the move's reservation does not carry takes over a reserved line of
     * another lot, on that lot's shelf: look up where it lies under the move's
     * source, so it is picked from there.
     */
    async locateLot() {
        const lotId = this.selectedLotIdNumber;
        this.state.lotLocation = null;
        this.state.lotMissing = false;
        if (!this.unreservedLot) {
            return;
        }
        const location = await this.barcodeScannerState.lotSourceLocation(
            this.state.move.product_id[0],
            lotId,
            this.state.move.location_id[0]
        );
        // The operator may have chosen another lot meanwhile.
        if (this.selectedLotIdNumber !== lotId) {
            return;
        }
        if (location) {
            this.state.lotLocation = {id: location[0], display_name: location[1]};
        } else {
            this.state.lotMissing = true;
        }
    }

    /**
     * Why the lot chosen cannot be picked: the reservation does not carry it and
     * it has no stock under the move's source. Choosing where it comes from (in
     * an internal transfer) is the operator's way past it.
     *
     * @returns {String} the reason, empty when there is none
     */
    get missingLotMessage() {
        if (!this.state.lotMissing || this.state.sourceLocation) {
            return "";
        }
        return _t("Lot %(lot)s has no stock in %(location)s.", {
            lot: this.selectedLot?.name || "",
            location: this.state.move?.location_id?.[1] || "",
        });
    }

    /**
     * Where the pick goes to, as shown: the location the operator chose,
     * otherwise that of the line it goes on (a putaway shelf, say).
     *
     * @returns {Object|null} the location, as id and display_name
     */
    get shownDestLocation() {
        return this.state.destLocation || this.lineLocation("location_dest_id");
    }

    /**
     * A location of the line the pick goes on: the reserved line worked on,
     * otherwise the move's first line with nothing picked yet; the move's when
     * it has none.
     *
     * @param {String} field location_id or location_dest_id
     * @returns {Object|null} the location, as id and display_name
     */
    lineLocation(field) {
        const line =
            this.targetLine ||
            (this.state.moveLines || []).find(
                (moveLine) => !(Number(moveLine.qty_picked) > 0)
            );
        const location = [line?.[field], this.state.move?.[field]].find(Array.isArray);
        return location ? {id: location[0], display_name: location[1]} : null;
    }

    /**
     * What the reservation still holds of a lot: what the move's lines reserve
     * of it, less what was picked of it on any of them. A lot over-picked on
     * one line is covered, whatever its other lines still reserve.
     *
     * @param {Object[]} moveLines the move's lines
     * @param {Number|false} lotId the lot's id, false for no lot
     * @returns {Number} the quantity still to pick of it
     */
    reservedLeft(moveLines, lotId) {
        return moveLines
            .filter((line) => lineLotId(line) === lotId)
            .reduce((sum, line) => sum + this.lineLeft(line), 0);
    }

    /**
     * What a line still holds: what it reserves, less what was picked on it.
     *
     * @param {Object} line a move line
     * @returns {Number} the quantity still to pick on it
     */
    lineLeft(line) {
        return (Number(line.quantity) || 0) - (Number(line.qty_picked) || 0);
    }

    get isOutgoing() {
        return this.props.params?.pickingTypeCode === "outgoing";
    }

    /**
     * Let the operator choose where stock comes from / goes to. Enabled for
     * receptions (put-away destination) and internal transfers; kept off for
     * deliveries, whose destination is the customer location and must not be
     * repointed to an internal one from here.
     */
    get canEditLocations() {
        return this.props.params?.pickingTypeCode !== "outgoing";
    }

    get moveId() {
        return this.props.params?.moveId;
    }

    get pickingId() {
        return this.props.params?.pickingId;
    }

    get listParams() {
        return this.props.params?.listParams || null;
    }

    get demandQty() {
        return this.state.move?.quantity || this.state.move?.product_uom_qty || 0;
    }

    get doneQty() {
        return Math.max(this.demandQty - this.remainingQty, 0);
    }

    get remainingQty() {
        return this.barcodeScannerState.getRemainingQty(this.moveId);
    }

    get canDecrement() {
        if (this.isSerial) return false;
        return (this.state.qtyPicked || 0) > 0;
    }

    get canIncrement() {
        if (this.isSerial) {
            return this.state.qtyPicked < 1 && !this.selectedLotIdNumber;
        }
        // Over-picking is allowed (Odoo puts no cap on done vs demand), so the
        // stepper can always add; the remaining figure stays informational.
        return true;
    }

    get targetLineId() {
        return this.targetLine?.id || false;
    }

    /**
     * What is left to pick here: what the reserved line it goes on still holds,
     * so that a move reserved over several lines is completed line by line;
     * otherwise, and always in receptions, what the whole move lacks.
     *
     * @returns {Number} the quantity left to pick
     */
    get pickableQty() {
        const line = this.targetLine;
        if (line) {
            return Math.min(this.lineLeft(line), this.remainingQty);
        }
        return this.remainingQty;
    }

    get canFulfill() {
        if (this.isSerial) return false;
        // Shown while anything is still missing, including the last unit: the
        // shortcut disappearing at 1 reads as "nothing left to pick".
        return this.pickableQty - (this.state.qtyPicked || 0) > 0;
    }

    get fulfillIncrement() {
        return Math.max(this.pickableQty - (this.state.qtyPicked || 0), 0);
    }

    get isTracked() {
        return this.state.tracking !== "none";
    }

    get hasLotGroup() {
        return user.hasGroup("stock.group_production_lot");
    }

    get isSerial() {
        return this.state.tracking === "serial";
    }

    get canCreateLot() {
        return this.isIncoming && this.isTracked && this.state.useCreateLots;
    }

    get canUseExistingLot() {
        return this.isTracked && this.state.useExistingLots;
    }

    get selectedLotIdNumber() {
        const lotId = parseInt(this.state.selectedLotId, 10);
        return Number.isNaN(lotId) ? null : lotId;
    }

    get selectedLot() {
        return (
            this.state.lots.find((lot) => lot.id === this.selectedLotIdNumber) || null
        );
    }

    get realLots() {
        return (this.state.lots || []).filter((lot) => lot.id > 0);
    }

    get headerEyebrow() {
        return this.isIncoming ? _t("Reception task") : _t("Picking task");
    }

    get headerSubtitle() {
        if (this.state.mode === "create_lot") {
            return _t("Create the lot first, then confirm the move in one pass.");
        }
        if (this.isTracked) {
            return _t("Select the correct lot or serial and confirm the quantity.");
        }
        return _t("Confirm the quantity and return to the picking queue.");
    }

    get trackingLabel() {
        const labels = {
            none: _t("No tracking"),
            lot: _t("Lot tracked"),
            serial: _t("Serial tracked"),
        };
        return labels[this.state.tracking] || _t("Tracking");
    }

    get lotFieldLabel() {
        return this.isSerial ? _t("Serial number") : _t("Lot number");
    }

    get quantityHelper() {
        if (this.isSerial) {
            return _t("Serial-tracked products can only process one unit.");
        }
        return `${this.pickableQty} ${_t("remaining to process")}`;
    }

    get confirmLabel() {
        return this.state.mode === "create_lot"
            ? _t("Create lot & confirm")
            : _t("Confirm move");
    }

    get backLabel() {
        return this.state.mode === "create_lot" ? _t("Back to pick") : _t("Back");
    }

    get modeDescription() {
        return this.state.mode === "create_lot"
            ? _t("Register a new lot before assigning the picked quantity.")
            : _t("Use an existing lot or serial already available for this product.");
    }

    get selectedLotExpirationLabel() {
        return this.selectedLot?.expiration_date || _t("No expiration date");
    }

    get selectedLotQtyLabel() {
        const qty = this.selectedLot?.product_qty;
        if (qty === undefined || qty === null || qty === false) {
            return _t("Qty unavailable");
        }
        return `${qty} ${_t("on hand")}`;
    }

    get quantityInputMax() {
        return this.isSerial ? 1 : undefined;
    }

    get todayDate() {
        return new Date().toISOString().split("T")[0];
    }

    getTodayStart() {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        return today;
    }

    isLotExpired(lot) {
        if (!lot?.expiration_date) {
            return false;
        }
        const expiration = new Date(lot.expiration_date);
        expiration.setHours(0, 0, 0, 0);
        return expiration < this.getTodayStart();
    }

    setMode(mode) {
        if (mode === "create_lot" && !this.canCreateLot) {
            return;
        }
        this.state.mode = mode;
    }

    adjustQty(delta) {
        if (this.state.loading) return;
        const next = (parseFloat(this.state.qtyPicked) || 0) + delta;
        if (this.isSerial) {
            this.state.qtyPicked = Math.max(0, Math.min(1, next));
        } else {
            this.state.qtyPicked = Math.max(0, Math.min(this.remainingQty, next));
        }
        this.state._lastInputSource = "tap";
    }

    /**
     * A quantity that arrives prefilled (a count carried by the scanned barcode)
     * still has to respect the serial rule, but it is NOT capped to the
     * remaining demand: over-picking is allowed, exactly as Odoo lets you
     * receive/process more than was ordered.
     */
    clampScannedQty(value) {
        const qty = parseFloat(value) || 1;
        if (this.isSerial) {
            return 1;
        }
        return qty;
    }

    setQty(value) {
        const qty = parseFloat(value);
        if (Number.isNaN(qty) || qty < 0) {
            this.state.qtyPicked = 0;
            return;
        }
        // Serial stays a single unit; anything else may exceed the demand
        // (over-picking is allowed, matching Odoo).
        this.state.qtyPicked = this.isSerial ? Math.min(qty, 1) : qty;
        this.state._lastInputSource = "tap";
    }

    fulfillRemaining() {
        if (!this.canFulfill) return;
        this.state.qtyPicked = this.pickableQty;
        this.state._lastInputSource = "tap";
        this.feedback.success({
            message: _t("Remaining quantity applied"),
            notify: true,
        });
    }

    onProductScanned(product) {
        if (!product) return;
        const moveProductId = this.state.move?.product_id?.[0];
        if (product.id === moveProductId) {
            this.feedback.success();
            return;
        }
        this.inventory.notify(
            _t(
                "Scanned product doesn't match this move (%(expected)s expected, got %(got)s)",
                {
                    expected: this.state.move?.product_id?.[1] || "",
                    got: product.display_name,
                }
            ),
            {type: "warning"}
        );
        this.feedback.warning();
    }

    onKeyDown(ev) {
        if (ev.target?.matches?.("input,textarea,[contenteditable]")) {
            return;
        }
        if (ev.key === "ArrowUp") {
            ev.preventDefault();
            this.adjustQty(1);
        } else if (ev.key === "ArrowDown") {
            ev.preventDefault();
            this.adjustQty(-1);
        } else if (ev.key === "f" || ev.key === "F") {
            if (this.canFulfill) {
                ev.preventDefault();
                this.fulfillRemaining();
            }
        }
    }

    onLotChange(ev) {
        this.state.selectedLotId = ev.target.value || null;
        return this.locateLot();
    }

    /**
     * Open the shared location picker, forwarding everything the wizard needs
     * to rebuild itself on return (it remounts) so the in-progress quantity,
     * lot and mode survive, plus both current location choices and which field
     * this selection targets. The picker writes the chosen location back under
     * `type` and returns here.
     */
    navigateToLocationSelector(type, locationDomain = null) {
        this.store.navigate("location_selector", {
            moveId: this.moveId,
            pickingId: this.pickingId,
            pickingTypeCode: this.props.params?.pickingTypeCode,
            listParams: this.listParams,
            defaultQty: this.state.qtyPicked,
            defaultLot: this.state.selectedLotId,
            lotName: this.state.newLotName,
            expiration: this.state.newLotExpirationDate,
            createLot: this.state.mode === "create_lot",
            moveSourceLocation: this.state.sourceLocation,
            moveDestLocation: this.state.destLocation,
            locationDomain,
            type,
        });
    }

    selectSourceLocation() {
        this.navigateToLocationSelector("moveSourceLocation");
    }

    selectDestLocation() {
        this.navigateToLocationSelector(
            "moveDestLocation",
            this.locationDomainFor("location_dest_id")
        );
    }

    // Restrict the destination picker to valid locations for this move -- exactly
    // Odoo's back-office domain for the move line "To": child_of the picking's own
    // destination, excluding view locations. Without it the picker offered every
    // internal location (any warehouse), and choosing one outside the operation's
    // warehouse silently reverted to the operation type default on validation.
    locationDomainFor(field) {
        const picking = this.barcodeScannerState.picking;
        const anchor =
            field === "location_dest_id"
                ? picking?.location_dest_id?.[0] ||
                  this.state.move?.location_dest_id?.[0]
                : picking?.location_id?.[0] || this.state.move?.location_id?.[0];
        if (!anchor) {
            return null;
        }
        return [
            ["id", "child_of", anchor],
            ["usage", "!=", "view"],
        ];
    }

    async loadData() {
        if (
            !this.barcodeScannerState.ready ||
            this.barcodeScannerState.activePickingId !== this.pickingId
        ) {
            await this.barcodeScannerState.preloadPicking(this.pickingId);
        }
        const moveId = this.moveId;
        const move = this.barcodeScannerState.getMove(moveId);
        const product = this.barcodeScannerState.getProduct(move.product_id[0]);
        const moveLines = this.barcodeScannerState.getMoveLinesForMove(moveId);

        this.state.useExistingLots = this.barcodeScannerState.useExistingLots;
        this.state.useCreateLots = this.barcodeScannerState.useCreateLots;

        let lots = this.barcodeScannerState.getLotsForProduct(move.product_id[0], {
            onlyAvailable: !this.isIncoming,
            excludeExpired: false,
        });

        if (!this.state.useExistingLots) {
            lots = [];
        }

        const defaultLotId = this.selectedLotIdNumber;
        if (defaultLotId && !lots.some((lot) => lot.id === defaultLotId)) {
            const defaultLot = this.barcodeScannerState.lotsById[defaultLotId];
            if (defaultLot) {
                lots = [defaultLot, ...lots];
            }
        }

        this.state.move = move;
        this.state.moveLines = moveLines;
        this.state.tracking = product.tracking;
        lots = this.preselectReservedLot(moveLines, lots);
        this.fitStartToLine();
        await this.locateLot();

        if (this.isTracked && this.isIncoming) {
            if (this.state.useCreateLots && !this.state.useExistingLots) {
                this.state.mode = "create_lot";
            } else if (this.state.useExistingLots && !this.state.useCreateLots) {
                this.state.mode = "pick";
            }
        }
        this.state.lots = lots || [];
        this.state.qtyPicked = this.clampScannedQty(this.state.qtyPicked);
        this.state.loading = false;
    }

    async ensureLotCreated() {
        if (!this.state.newLotName) {
            this.inventory.notify(_t("Lot name required"), {type: "danger"});
            return null;
        }
        if (
            this.isSerial &&
            this.state.lots.some(
                (lot) => lot.name?.toLowerCase() === this.state.newLotName.toLowerCase()
            )
        ) {
            this.inventory.notify(_t("Serial already exists for this product."), {
                type: "danger",
            });
            return null;
        }
        const lot = this.barcodeScannerState.stageLotCreate({
            productId: this.state.move.product_id[0],
            name: this.state.newLotName,
            expirationDate: this.state.newLotExpirationDate || false,
        });
        this.state.lots = [
            ...this.state.lots.filter((item) => item.id !== lot.id),
            lot,
        ];
        this.state.selectedLotId = String(lot.id);
        return lot;
    }

    async confirmPick() {
        if (this.state.mode === "create_lot" && !this.isIncoming) {
            this.inventory.notify(_t("Lots can only be created in receptions"), {
                type: "danger",
            });
            return;
        }
        if (this.state.mode === "create_lot" && !this.state.selectedLotId) {
            const lot = await this.ensureLotCreated();
            if (!lot) {
                return;
            }
        }
        if (!this.state.qtyPicked || this.state.qtyPicked <= 0) {
            this.inventory.notify(_t("Invalid quantity"), {type: "danger"});
            return;
        }
        if (
            this.state.tracking === "serial" &&
            parseFloat(this.state.qtyPicked) !== 1
        ) {
            this.inventory.notify(
                _t("Serial-tracked products must have a quantity of 1."),
                {type: "danger"}
            );
            return;
        }
        if (
            this.state.tracking !== "none" &&
            (this.canUseExistingLot || this.canCreateLot) &&
            !this.selectedLotIdNumber &&
            this.state.mode !== "create_lot"
        ) {
            this.inventory.notify(_t("Please select a lot"), {type: "danger"});
            return;
        }
        const missingLot = this.missingLotMessage;
        if (missingLot) {
            this.inventory.notify(missingLot, {type: "danger"});
            return;
        }

        const guardrailError = this.barcodeScannerSync.validateConfirmMovePayload({
            productId: this.state.move.product_id[0],
            lotId: this.selectedLotIdNumber || false,
            lotName: this.selectedLot
                ? this.selectedLot.name
                : this.state.newLotName || false,
            qtyPicked: this.state.qtyPicked,
            createLot: this.state.mode === "create_lot",
            expirationDate: this.state.newLotExpirationDate || false,
            moveId: this.moveId,
        });
        if (guardrailError) {
            this.inventory.notify(guardrailError.message, {type: "danger"});
            return;
        }
        const lot = this.selectedLot;
        // Receptions and internal moves may use an expired lot (it records what
        // arrived / relocates it); only a delivery to a customer is blocked.
        if (this.isLotExpired(lot) && this.isOutgoing) {
            this.inventory.notify(_t("Lot expired"), {type: "danger"});
            return;
        }

        if (this.unreservedLot) {
            if (!(await this.pickUnreservedLot())) {
                return;
            }
        } else {
            await this.confirmOnLine(lot);
        }
        // Hand the move back so the picking screen opens on the tab that
        // now holds it: still "To Do" while quantity is missing, "Done" once
        // this confirmation completed it.
        this.store.navigate(
            "picking",
            {
                pickingId: this.pickingId,
                listParams: this.listParams,
                reloadToken: Date.now(),
                focusMoveId: this.moveId,
            },
            {replace: true}
        );
    }

    /**
     * Stage the pick on the move's lines: the reserved one the wizard works on
     * and those after it, or a line of the lot.
     *
     * @param {Object|null} lot the lot chosen
     */
    async confirmOnLine(lot) {
        await this.barcodeScannerSync.confirmMove({
            moveId: this.moveId,
            moveLineId: this.targetLineId,
            pickingId: this.pickingId,
            productId: this.state.move.product_id[0],
            qtyPicked: this.state.qtyPicked,
            lotId: this.selectedLotIdNumber || false,
            lotName: lot ? lot.name : this.state.newLotName || false,
            createLot: this.state.mode === "create_lot",
            expirationDate: this.state.newLotExpirationDate || false,
            // Only a location the operator chose: otherwise the line keeps
            // where Odoo reserved its stock, and its putaway shelf.
            locationId: this.sourceLocationId,
            locationDestId: this.state.destLocation?.id || false,
        });
    }

    async goBack() {
        if (this.state.mode === "create_lot" && this.canUseExistingLot) {
            this.setMode("pick");
            return;
        }

        this.store.navigate(
            "picking",
            {
                pickingId: this.pickingId,
                listParams: this.listParams,
                reloadToken: Date.now(),
            },
            {replace: true}
        );
    }

    toggleCreateLot() {
        this.setMode(this.state.mode === "pick" ? "create_lot" : "pick");
    }
}

MoveWizardScreen.template = "barcode_scanner.MoveWizardScreen";
MoveWizardScreen.props = {
    params: {type: Object, optional: true},
    navigate: {type: Function, optional: true},
};

barcodeScreens.add("move_wizard", {component: MoveWizardScreen});
