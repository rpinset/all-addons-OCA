import {Component, onWillStart, onWillUpdateProps, useState} from "@odoo/owl";
import {ConfirmationDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {PickingDoneList} from "@barcode_stock/js/components/picking_done_list.esm";
import {PickingInfoTab} from "@barcode_stock/js/components/picking_info_tab.esm";
import {PickingMoveList} from "@barcode_stock/js/components/picking_move_list.esm";
import {_t} from "@web/core/l10n/translation";
import {barcodeMatchDomain} from "@barcode_scanner/js/utils/scan_match.esm";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {tabForMove} from "@barcode_stock/js/utils/move_progress.esm";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useService} from "@web/core/utils/hooks";

export class PickingScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.feedback = useService("barcodeScannerFeedback");
        this.barcodeScannerState = useService("barcodeScannerState");
        this.barcodeScannerSync = useService("barcodeScannerSync");
        this.setTab = this.setTab.bind(this);
        this.deleteMoveLine = this.deleteMoveLine.bind(this);
        this.openMoveWizard = this.openMoveWizard.bind(this);
        this.onBarcodeScanned = this.onBarcodeScanned.bind(this);
        useBarcodeHandler({
            onScan: (barcode, parsedData, payload) => {
                this.onBarcodeScanned(barcode, parsedData, payload);
            },
        });

        this.selectResponsible = this.selectResponsible.bind(this);

        this.state = useState({
            picking: null,
            moves: [],
            moveLines: [],
            activeTab: "todo",
            isValidating: false,
            isSaving: false,
            pickingTypeCode: null,
            highlightedMoveId: null,
            lastScan: {
                barcode: "",
                source: "",
                tone: "idle",
                message: _t("Scanner ready for this picking."),
                productName: "",
                lotName: "",
                quantity: 0,
                timestamp: null,
            },
        });

        onWillStart(async () => {
            try {
                const responsible = this.props.params?.responsible;
                if (responsible && responsible.id && this.pickingId) {
                    await this.inventory.write("stock.picking", [this.pickingId], {
                        user_id: responsible.id,
                    });
                }
                // A move confirmed in the wizard comes back as the move
                // to focus, so the reload below lands on its tab.
                this.state.highlightedMoveId = this.focusMoveId;
                // Coming back from another screen (the responsible picker,
                // say) should land on the tab it was opened from, not on the
                // default one.
                const returnedTab = this.props.params?.activeTab;
                if (returnedTab) {
                    this.state.activeTab = returnedTab;
                }
                await this.loadData({force: true});
                if (responsible && responsible.id) {
                    this.state.activeTab = "info";
                    this.inventory.notify(
                        _t("Responsible set to %(name)s", {name: responsible.name}),
                        {
                            type: "success",
                        }
                    );
                }
            } catch (error) {
                this.inventory.notify(_t("Error loading picking: %(error)s", {error}), {
                    type: "danger",
                });
            }
        });

        onWillUpdateProps(async (nextProps) => {
            const currentId = this.props.pickingId || this.props.params?.pickingId;
            const nextId = nextProps.pickingId || nextProps.params?.pickingId;
            const currentReloadToken =
                this.props.reloadToken || this.props.params?.reloadToken;
            const nextReloadToken =
                nextProps.reloadToken || nextProps.params?.reloadToken;

            if (currentId !== nextId || currentReloadToken !== nextReloadToken) {
                this.state.highlightedMoveId =
                    nextProps.focusMoveId || nextProps.params?.focusMoveId || null;
                await this.loadData({force: true});
            }
        });
    }

    get pickingId() {
        return this.props.pickingId || this.props.params?.pickingId;
    }

    get focusMoveId() {
        return this.props.focusMoveId || this.props.params?.focusMoveId || null;
    }

    get listParams() {
        return this.props.listParams || this.props.params?.listParams || null;
    }

    get operationLabel() {
        const labels = {
            incoming: _t("Receipt"),
            internal: _t("Internal Transfer"),
            outgoing: _t("Delivery Order"),
        };
        return labels[this.state.pickingTypeCode] || _t("Picking");
    }

    get doneLines() {
        return this.state.moveLines.filter((line) => (line.qty_picked || 0) > 0);
    }

    get moveStatsById() {
        const moveLineTotals = this.state.moveLines.reduce((totals, line) => {
            const moveId = line.move_id?.[0];
            if (!moveId) {
                return totals;
            }
            totals[moveId] = (totals[moveId] || 0) + (line.qty_picked || 0);
            return totals;
        }, {});

        return Object.fromEntries(
            this.state.moves.map((move) => {
                const demandQty = move.product_uom_qty || move.quantity || 0;
                const reservedQty = move.quantity || 0;
                const doneQty = moveLineTotals[move.id] || 0;
                const remainingQty = Math.max(reservedQty - doneQty, 0);
                const completion = demandQty ? Math.min(doneQty / demandQty, 1) : 0;
                return [
                    move.id,
                    {
                        demandQty,
                        doneQty,
                        remainingQty,
                        completion,
                        completionLabel: `${Math.round(completion * 100)}%`,
                    },
                ];
            })
        );
    }

    get pendingMovesCount() {
        return this.state.moves.filter(
            (move) => (this.moveStatsById[move.id]?.remainingQty || 0) > 0
        ).length;
    }

    get completedMovesCount() {
        return this.state.moves.filter(
            (move) => (this.moveStatsById[move.id]?.remainingQty || 0) <= 0
        ).length;
    }

    get progressSummary() {
        const summary = Object.values(this.moveStatsById).reduce(
            (acc, stats) => {
                acc.demandQty += stats.demandQty || 0;
                acc.doneQty += stats.doneQty || 0;
                acc.remainingQty += stats.remainingQty || 0;
                return acc;
            },
            {demandQty: 0, doneQty: 0, remainingQty: 0}
        );
        summary.percent = summary.demandQty
            ? Math.round((summary.doneQty / summary.demandQty) * 100)
            : 0;
        return summary;
    }

    get summaryCards() {
        return [
            {
                key: "pending",
                label: _t("Pending moves"),
                value: this.pendingMovesCount,
                tone: "warning",
            },
            {
                key: "done",
                label: _t("Done lines"),
                value: this.doneLines.length,
                tone: "success",
            },
            {
                key: "progress",
                label: _t("Progress"),
                value: `${this.progressSummary.percent}%`,
                tone: "info",
            },
        ];
    }

    setLastScanContext({
        barcode = "",
        source = "hardware",
        tone = "info",
        message = "",
        move = null,
        quantity = 0,
        lotName = "",
    } = {}) {
        this.state.lastScan = {
            barcode,
            source,
            tone,
            message,
            productName: move?.product_id?.[1] || "",
            lotName,
            quantity,
            timestamp: Date.now(),
        };
        this.state.highlightedMoveId = move?.id || null;
        this.focusScannedMove();
    }

    /**
     * Show the tab that actually holds the highlighted move. A move still
     * pending lives in "To Do"; once it is fully picked only "Done" lists it,
     * so switching to "To Do" after every scan left the operator in front of a
     * list without the line the notification had just confirmed.
     */
    focusScannedMove() {
        const moveId = this.state.highlightedMoveId;
        if (!moveId) {
            return;
        }
        const move = this.state.moves.find((candidate) => candidate.id === moveId);
        if (!move) {
            return;
        }
        this.state.activeTab = tabForMove(move);
    }

    async loadData({force = false} = {}) {
        const pickingId = this.pickingId;
        if (
            force ||
            !(
                this.barcodeScannerState.ready &&
                this.barcodeScannerState.activePickingId === pickingId
            )
        ) {
            await this.barcodeScannerState.preloadPicking(pickingId);
        }
        const snapshot = this.barcodeScannerState.getSnapshot();
        const picking = snapshot.picking || {};
        this.state.pickingTypeCode = snapshot.pickingTypeCode;
        this.state.moves = await this.buildMovesWithLots(snapshot.moves || []);
        this.state.picking = {...picking};
        this.state.moveLines = [...(snapshot.moveLines || [])];
        if (picking.scheduled_date) {
            this.state.picking.scheduled_date = picking.scheduled_date
                .replace(" ", "T")
                .slice(0, 16);
        }
        // The scanned line may have just become complete, which moves it from
        // one tab to the other; decide again on the data that was just read.
        this.focusScannedMove();
    }

    setTab(tab) {
        this.state.activeTab = tab;
    }

    goBack() {
        this.store.goBack();
    }

    selectResponsible() {
        this.store.navigate("user_selector", {
            returnRoute: "picking",
            returnParams: {
                pickingId: this.pickingId,
                listParams: this.listParams,
                activeTab: this.state.activeTab,
            },
        });
    }

    async savePicking() {
        if (!this.state.picking?.id) return;
        this.state.isSaving = true;
        try {
            await this.barcodeScannerSync.stagePicking(
                {
                    scheduled_date: this.state.picking.scheduled_date || false,
                    note: this.state.picking.note || false,
                },
                {immediate: true}
            );
            this.inventory.notify(_t("Changes saved successfully"), {
                type: "success",
            });
        } catch {
            this.inventory.notify(_t("Error while saving"), {
                type: "danger",
            });
        } finally {
            this.state.isSaving = false;
        }
    }

    async validatePicking() {
        if (!this.state.picking?.id) return;

        if (!this.checkAnyMoveLineWithQty()) {
            this.inventory.notify(_t("Please add at least one product to validate."), {
                type: "danger",
            });
            return;
        }

        const guardrailErrors = this.barcodeScannerSync.validatePickingForConfirm();
        if (guardrailErrors.length > 0) {
            for (const err of guardrailErrors) {
                this.inventory.notify(err.message, {type: "danger"});
            }
            return;
        }

        this.state.isValidating = true;
        try {
            await this.savePicking();
            const action = await this.inventory.call(
                "stock.picking",
                "button_validate",
                [this.state.picking.id],
                {context: {active_ids: [this.state.picking.id]}}
            );
            if (
                action &&
                action.type === "ir.actions.act_window" &&
                action.res_model === "stock.backorder.confirmation"
            ) {
                await this.action.doAction(action, {
                    onClose: () => {
                        this.store.navigate("picking_list", this.listParams || {}, {
                            clearHistory: true,
                        });
                    },
                });
            } else if (action && action.type === "ir.actions.act_window") {
                await this.action.doAction(action);
                this.store.navigate("picking_list", this.listParams || {}, {
                    clearHistory: true,
                });
            } else {
                this.store.navigate("picking_list", this.listParams || {}, {
                    clearHistory: true,
                });
            }
        } catch (error) {
            this.inventory.notify(
                _t("Validation failed: %(error)s", {error: error.message}),
                {
                    type: "danger",
                }
            );
        } finally {
            this.state.isValidating = false;
        }
    }

    async _reloadMoves() {
        await this.loadData({force: true});
    }

    async cancelReservation() {
        this.dialog.add(ConfirmationDialog, {
            title: _t("Confirm cancel reservations"),
            body: _t("Are you sure you want to cancel reservations?"),
            confirm: async () => {
                try {
                    this.state.highlightedMoveId = null;
                    await this.inventory.write(
                        "stock.move.line",
                        this.state.moveLines.map((ml) => ml.id),
                        {qty_picked: 0}
                    );
                    await this.inventory.call("stock.picking", "do_unreserve", [
                        [this.pickingId],
                    ]);
                    this.inventory.notify(_t("Cancel Reservation successfully"), {
                        type: "success",
                    });
                } catch (error) {
                    this.inventory.notify(
                        _t("Cancel Reservation error: %(error)s", {error}),
                        {
                            type: "error",
                        }
                    );
                }
                await this._reloadMoves();
            },
        });
    }

    async checkAvailability() {
        this.dialog.add(ConfirmationDialog, {
            title: _t("Confirm availability check"),
            body: _t("Are you sure you want to check availability?"),
            confirm: async () => {
                try {
                    await this.inventory.call("stock.picking", "action_assign", [
                        [this.pickingId],
                    ]);
                    this.inventory.notify(_t("Availability check successful."), {
                        type: "success",
                    });
                    await this._reloadMoves();
                } catch (error) {
                    this.inventory.notify(
                        _t("Availability check error: %(error)s", {error}),
                        {
                            type: "error",
                        }
                    );
                }
            },
        });
    }

    openMoveWizard(move, defaults = {}) {
        if (move.quantity === 0) {
            this.inventory.notify(_t("This move has no quantity to process."), {
                type: "warning",
            });
            return;
        }
        this.store.navigate("move_wizard", {
            moveId: move.id,
            pickingId: this.state.picking.id,
            pickingTypeCode: this.state.pickingTypeCode,
            defaultQty: defaults.qty || 1,
            defaultLot: defaults.lot || null,
            lotName: defaults.lotName || null,
            expiration: defaults.expiration || null,
            createLot: defaults.createLot || false,
            listParams: this.listParams,
        });
    }

    async deleteMoveLine(moveLineId) {
        this.dialog.add(ConfirmationDialog, {
            title: _t("Confirm deletion"),
            body: _t("Are you sure you want to delete this movement?"),
            confirm: async () => {
                // Undoing a confirmation voids the scan that produced it, so
                // the reload below must not chase the line to another tab.
                this.state.highlightedMoveId = null;
                await this.barcodeScannerSync.resetMoveLine(moveLineId, {
                    immediate: true,
                });
                this.state.moveLines = this.state.moveLines.filter(
                    (l) => l.id !== moveLineId
                );
                await this._reloadMoves();
            },
        });
    }

    async createMoveLine(moveId, productId, qty, lotId = null) {
        const move = this.barcodeScannerState.getMove(moveId);
        const lot = lotId ? this.barcodeScannerState.lotsById[lotId] : null;
        await this.barcodeScannerSync.confirmMove({
            moveId,
            pickingId: this.state.picking.id,
            productId,
            qtyPicked: qty,
            lotId: lotId || false,
            lotName: lot?.name || false,
            locationId: move?.location_id?.[0] || false,
            locationDestId: move?.location_dest_id?.[0] || false,
        });

        await this._reloadMoves();

        this.inventory.notify(_t("Product updated"), {
            type: "success",
        });
    }

    async openMoveForProduct(barcode, preselectedMove = null, {qty = 1} = {}) {
        if (preselectedMove) {
            this.setLastScanContext({
                barcode,
                tone: "success",
                message: _t("Product matched and ready to confirm."),
                move: preselectedMove,
                quantity: qty,
            });
            this.openMoveWizard(preselectedMove, {
                qty,
            });
            return;
        }
        const productDomain = barcodeMatchDomain(barcode);
        const products = productDomain
            ? await this.inventory.searchRead("product.product", productDomain, [
                  "display_name",
                  "tracking",
              ])
            : [];
        if (!products.length) {
            this.setLastScanContext({
                barcode,
                tone: "warning",
                message: _t("Scanned product was not found."),
            });
            this.inventory.notify(_t("Product not found"), {type: "danger"});
            return;
        }
        const product = products[0];
        const move = this.state.moves.find((m) => m.product_id?.[0] === product.id);
        if (!move) {
            this.setLastScanContext({
                barcode,
                tone: "warning",
                message: _t("This product is not reserved for this picking."),
            });
            this.inventory.notify(_t("Product not reserved"), {
                type: "warning",
            });
            return;
        }
        this.setLastScanContext({
            barcode,
            tone: "success",
            message: _t("Product matched and ready to confirm."),
            move,
            quantity: qty,
        });
        this.openMoveWizard(move, {
            qty,
        });
    }

    /**
     * A scan carrying a lot or serial number opens the wizard with it already
     * resolved: a known lot is preselected, and a lot the operation cannot pick
     * from stock goes through the create-lot flow — available on receipts only,
     * the one operation allowed to register lots.
     */
    async handleScannedLot(move, normalized, source) {
        const {barcode, lot, quantity, expiration} = normalized;
        const lotName = lot?.name || normalized.lotName;
        const isOutgoing = this.state.pickingTypeCode === "outgoing";
        const today = new Date().toISOString().slice(0, 10);
        const expired =
            (lot && this.barcodeScannerState.isLotExpired(lot.id)) ||
            (expiration && expiration < today);
        if (expired) {
            const message = _t("Lot %(lot)s has passed its expiration date.", {
                lot: lotName,
            });
            this.feedback.warning({notify: true, message});
            // A reception records what physically arrived and an internal move
            // just relocates the stock, so both warn and let the scan proceed;
            // only a delivery to a customer stays a hard stop.
            if (isOutgoing) {
                this.setLastScanContext({
                    barcode,
                    source,
                    tone: "warning",
                    message,
                    move,
                    lotName,
                });
                return;
            }
        }
        if (lot && this.barcodeScannerState.useExistingLots) {
            this.setLastScanContext({
                barcode,
                source,
                tone: "success",
                message: _t("Lot %(lot)s matched and ready to confirm.", {
                    lot: lot.name,
                }),
                move,
                quantity,
                lotName: lot.name,
            });
            this.openMoveWizard(move, {
                qty: quantity,
                lot: lot.id,
                lotName: lot.name,
            });
            return;
        }

        const canCreateLot =
            this.state.pickingTypeCode === "incoming" &&
            this.barcodeScannerState.useCreateLots;
        if (!canCreateLot) {
            const message = _t("Lot %(lot)s is not available for this product.", {
                lot: lotName,
            });
            this.setLastScanContext({
                barcode,
                source,
                tone: "warning",
                message,
                move,
                lotName,
            });
            this.feedback.warning({notify: true, message});
            return;
        }
        this.setLastScanContext({
            barcode,
            source,
            tone: "success",
            message: _t("Lot %(lot)s ready to be registered.", {lot: lotName}),
            move,
            quantity,
            lotName,
        });
        this.openMoveWizard(move, {
            qty: quantity,
            lotName,
            expiration,
            createLot: true,
        });
    }

    onBarcodeScanned(barcode, parsedData = null, payload = {}) {
        this.handleBarcode(barcode, parsedData, payload);
    }

    async handleBarcode(barcode, parsedData = null, payload = {}) {
        const normalized = this.barcodeScannerState.applyScanResult({
            barcode,
            ...(parsedData || {}),
        });
        const candidateMove = normalized.candidates[0] || null;
        const source = payload?.source || "hardware";
        if (!normalized.candidates.length) {
            this.setLastScanContext({
                barcode,
                source,
                tone: "warning",
                message: _t("Scanned barcode is not part of the current picking."),
            });
            this.feedback.warning({
                notify: true,
                message: _t("Scanned barcode is not part of the current picking."),
            });
            return;
        }

        const productId = candidateMove.product_id?.[0];
        const tracking =
            this.barcodeScannerState.indexes.trackingByProductId[productId];
        // The scan states how much it represents (one unit for a plain product
        // barcode, a count or a net weight for a barcode that carries one).
        const scannedQty = normalized.quantity;
        if (tracking === "none") {
            const existingLine = this.state.moveLines.find(
                (line) =>
                    line.move_id?.[0] === candidateMove.id &&
                    line.product_id?.[0] === productId &&
                    (line.qty_picked || 0) > 0
            );
            if (existingLine) {
                // NewQty is the resulting total, only used for the feedback
                // message below. confirmMove()/stageMoveLine() already increment
                // the existing line by the qtyPicked it receives, so pass the
                // scanned delta here -- passing the total would add the existing
                // quantity a second time (a re-scan jumped by +2 instead of +1).
                const newQty = (existingLine.qty_picked || 0) + scannedQty;
                await this.barcodeScannerSync.confirmMove({
                    moveId: candidateMove.id,
                    pickingId: this.state.picking.id,
                    productId,
                    qtyPicked: scannedQty,
                    lotId: false,
                    lotName: false,
                    locationId: candidateMove.location_id?.[0] || false,
                    locationDestId: candidateMove.location_dest_id?.[0] || false,
                });
                this.setLastScanContext({
                    barcode,
                    source,
                    tone: "success",
                    message: _t("Quantity incremented to %(qty)s.", {qty: newQty}),
                    move: candidateMove,
                    quantity: newQty,
                });
                this.feedback.success({
                    notify: true,
                    message: _t("Quantity incremented to %(qty)s.", {qty: newQty}),
                });
                await this._reloadMoves();
                return;
            }
        } else if (normalized.lotName) {
            await this.handleScannedLot(candidateMove, normalized, source);
            return;
        }

        await this.openMoveForProduct(barcode, candidateMove, {qty: scannedQty});
        if (payload?.source === "camera" && candidateMove) {
            this.feedback.success();
        }
    }

    async buildMovesWithLots(moves) {
        const lotsMap = Object.fromEntries(
            Object.values(this.barcodeScannerState.lotsById).map((lot) => [
                lot.id,
                lot.name,
            ])
        );
        return moves.map((move) => ({
            ...move,
            lot_names: (move.lot_ids || []).map((id) => lotsMap[id]),
        }));
    }

    checkAnyMoveLineWithQty() {
        return this.state.moveLines.some((line) => line.qty_picked > 0);
    }
}

PickingScreen.template = "barcode_scanner.PickingScreen";
PickingScreen.components = {PickingInfoTab, PickingMoveList, PickingDoneList};

barcodeScreens.add("picking", {
    component: PickingScreen,
    props: (params) => ({
        pickingId: params.pickingId,
        listParams: params.listParams || null,
        reloadToken: params.reloadToken || null,
        focusMoveId: params.focusMoveId || null,
        params,
    }),
});
