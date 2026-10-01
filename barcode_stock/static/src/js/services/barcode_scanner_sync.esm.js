import {Mutex} from "@web/core/utils/concurrency";
import {debounce} from "@web/core/utils/timing";
import {registry} from "@web/core/registry";

export const GUARDRAIL_CODES = {
    LOT_REQUIRED: "lot_required",
    LOT_EXPIRED: "lot_expired",
    SERIAL_QTY_INVALID: "serial_qty_invalid",
    SERIAL_DUPLICATE: "serial_duplicate",
    LOT_NAME_EMPTY: "lot_name_empty",
    LOT_NAME_DUPLICATE: "lot_name_duplicate",
    QTY_INVALID: "qty_invalid",
    QTY_EXCEEDS_REMAINING: "qty_exceeds_remaining",
};

function serializePickingValues(values) {
    return {
        ...values,
        scheduled_date: values.scheduled_date
            ? values.scheduled_date.replace("T", " ") + ":00"
            : false,
    };
}

export class BarcodeScannerSync {
    constructor(orm, barcodeScannerState) {
        this.orm = orm;
        this.state = barcodeScannerState;
        this.mutex = new Mutex();
        this.debouncedFlush = debounce(() => this.flush(), 400);
    }

    schedule() {
        if (this.state.sync.queue.length) {
            this.debouncedFlush();
        }
    }

    async stagePicking(values, {immediate = false} = {}) {
        this.state.stagePickingUpdate(values);
        if (immediate) {
            return this.flush();
        }
        this.schedule();
        return null;
    }

    async confirmMove(payload, {immediate = true} = {}) {
        let lot = null;
        if (payload.createLot) {
            lot = this.state.stageLotCreate({
                productId: payload.productId,
                name: payload.lotName,
                expirationDate: payload.expirationDate || false,
            });
        } else if (payload.lotId) {
            lot = this.state.lotsById[payload.lotId] || null;
        }

        const moveLine = this.state.stageMoveLine({
            moveId: payload.moveId,
            pickingId: payload.pickingId,
            productId: payload.productId,
            qtyPicked: payload.qtyPicked,
            lotId: lot?.id || payload.lotId || false,
            lotName: lot?.name || payload.lotName || false,
            locationId: payload.locationId,
            locationDestId: payload.locationDestId,
            extraValues: payload.extraValues || {},
        });

        if (immediate) {
            await this.flush();
        } else {
            this.schedule();
        }
        return {lot, moveLine};
    }

    async resetMoveLine(moveLineId, {immediate = true} = {}) {
        this.state.stageMoveLineReset(moveLineId);
        if (immediate) {
            return this.flush();
        }
        this.schedule();
        return null;
    }

    async flush() {
        return this.mutex.exec(async () => {
            const queue = [...this.state.sync.queue];
            if (!queue.length) {
                this.state.markSyncDone();
                return [];
            }

            this.state.sync.queue = [];
            this.state.markSyncRunning();

            try {
                for (const operation of queue) {
                    await this.flushOperation(operation, queue);
                }
                this.state.markSyncDone();
                if (this.state.sync.queue.length) {
                    this.schedule();
                }
                return queue;
            } catch (error) {
                this.state.sync.queue = [...queue, ...this.state.sync.queue];
                this.state.markSyncFailed(error);
                throw error;
            }
        });
    }

    updateQueuedLotReferences(queue, tempId, lot) {
        for (const operation of queue) {
            if (operation.values?.lot_id === tempId) {
                operation.values = {
                    ...operation.values,
                    lot_id: lot.id,
                    lot_name: lot.name,
                };
            }
        }
    }

    async flushOperation(operation, queue) {
        switch (operation.type) {
            case "picking_write":
                await this.orm.write(
                    "stock.picking",
                    [operation.pickingId],
                    serializePickingValues(operation.values)
                );
                return;
            case "lot_create": {
                const readFields = ["name", "product_id", "product_qty"];
                if (this.state.hasProductExpiry) {
                    readFields.push("expiration_date", "removal_date");
                }
                // A create-lots reception does not preload existing lots, so the
                // same batch scanned twice (two boxes of one lot) would try to
                // create a duplicate and hit the name+product uniqueness
                // constraint. There is exactly one lot record per name+product,
                // so reuse it when it exists and only create when it does not.
                const {name, product_id: productId} = operation.values;
                const existing =
                    name && productId
                        ? await this.orm.searchRead(
                              "stock.lot",
                              [
                                  ["name", "=", name],
                                  ["product_id", "=", productId],
                              ],
                              readFields,
                              {limit: 1}
                          )
                        : [];
                let lot = existing[0];
                if (!lot) {
                    const lotIds = await this.orm.create("stock.lot", [
                        operation.values,
                    ]);
                    const lotId = Array.isArray(lotIds) ? lotIds[0] : lotIds;
                    [lot] = await this.orm.read("stock.lot", [lotId], readFields);
                }
                this.state.replaceTemporaryLot(operation.tempId, lot);
                this.updateQueuedLotReferences(queue, operation.tempId, lot);
                return;
            }
            case "qty_update":
            case "move_line_write":
                await this.orm.write(
                    "stock.move.line",
                    [operation.moveLineId],
                    operation.values
                );
                return;
            case "move_line_create": {
                const moveLineIds = await this.orm.create("stock.move.line", [
                    operation.values,
                ]);
                const moveLineId = Array.isArray(moveLineIds)
                    ? moveLineIds[0]
                    : moveLineIds;
                this.state.replaceTemporaryMoveLineId(operation.tempId, moveLineId);
                return;
            }
        }
    }

    validateConfirmMovePayload(payload) {
        const {productId, lotId, lotName, qtyPicked, createLot} = payload;
        const tracking = this.state.indexes.trackingByProductId[productId];

        if (tracking === "none") {
            return null;
        }

        if (createLot) {
            const trimmedName = (lotName || "").trim();
            if (!trimmedName) {
                return {
                    code: GUARDRAIL_CODES.LOT_NAME_EMPTY,
                    message: "Lot name is required.",
                };
            }
        }

        if (!createLot && !lotId && tracking !== "none") {
            return {
                code: GUARDRAIL_CODES.LOT_REQUIRED,
                message: "A lot must be selected for this tracked product.",
            };
        }

        // Receptions and internal moves may use an expired lot -- a reception
        // records what physically arrived, and an internal transfer just
        // relocates it (e.g. to quarantine); both warn instead of blocking.
        // Only a delivery to a customer is a hard stop.
        if (
            lotId &&
            this.state.isLotExpired(lotId) &&
            this.state.pickingTypeCode === "outgoing"
        ) {
            return {
                code: GUARDRAIL_CODES.LOT_EXPIRED,
                message: "This lot has passed its expiration date and cannot be used.",
            };
        }

        if (tracking === "serial") {
            const qty = parseFloat(qtyPicked || 0);
            if (qty !== 1) {
                return {
                    code: GUARDRAIL_CODES.SERIAL_QTY_INVALID,
                    message: "Serial-tracked products must have quantity of 1.",
                };
            }
            if (!createLot && lotId) {
                const existingLines = this.state.getMoveLinesForMove(payload.moveId);
                const alreadyUsed = existingLines.some(
                    (line) => line.lot_id?.[0] === lotId && line.qty_picked > 0
                );
                if (alreadyUsed) {
                    return {
                        code: GUARDRAIL_CODES.SERIAL_DUPLICATE,
                        message:
                            "This serial number has already been used in this picking.",
                    };
                }
            }
            if (createLot && lotName) {
                const existingSerials = this.state.getLotsForProduct(productId, {
                    onlyAvailable: false,
                    excludeExpired: false,
                });
                const duplicate = existingSerials.some(
                    (lot) =>
                        lot.id > 0 && lot.name?.toLowerCase() === lotName.toLowerCase()
                );
                if (duplicate) {
                    return {
                        code: GUARDRAIL_CODES.SERIAL_DUPLICATE,
                        message:
                            "A serial number with this name already exists for this product.",
                    };
                }
            }
        }

        return null;
    }

    validateQtyUpdate(qtyPicked) {
        const qty = parseFloat(qtyPicked || 0);
        if (isNaN(qty) || qty < 0) {
            return {
                code: GUARDRAIL_CODES.QTY_INVALID,
                message: "Quantity must be a non-negative number.",
            };
        }
        return null;
    }

    validateLotCreate(productId, name) {
        const trimmedName = (name || "").trim();
        if (!trimmedName) {
            return {
                code: GUARDRAIL_CODES.LOT_NAME_EMPTY,
                message: "Lot name is required.",
            };
        }
        const tracking = this.state.indexes.trackingByProductId[productId];
        if (tracking === "serial") {
            const existingLots = this.state.getLotsForProduct(productId, {
                onlyAvailable: false,
                excludeExpired: false,
            });
            const duplicate = existingLots.some(
                (lot) =>
                    lot.id > 0 && lot.name?.toLowerCase() === trimmedName.toLowerCase()
            );
            if (duplicate) {
                return {
                    code: GUARDRAIL_CODES.SERIAL_DUPLICATE,
                    message: "A serial number with this name already exists.",
                };
            }
        }
        return null;
    }

    validatePickingForConfirm() {
        const errors = [];
        for (const moveLine of this.state.moveLines) {
            const productId = moveLine.product_id?.[0];
            const lotId = moveLine.lot_id?.[0];
            const qtyPicked = moveLine.qty_picked;
            const tracking = this.state.indexes.trackingByProductId[productId];

            if (!qtyPicked || qtyPicked <= 0) {
                continue;
            }

            if (
                lotId &&
                this.state.isLotExpired(lotId) &&
                this.state.pickingTypeCode === "outgoing"
            ) {
                errors.push({
                    code: GUARDRAIL_CODES.LOT_EXPIRED,
                    message: `Line for ${
                        moveLine.product_id?.[1] || "product"
                    } uses an expired lot.`,
                });
            }

            if (tracking === "serial" && parseFloat(qtyPicked) !== 1) {
                errors.push({
                    code: GUARDRAIL_CODES.SERIAL_QTY_INVALID,
                    message: `Line for ${
                        moveLine.product_id?.[1] || "product"
                    } has qty ${qtyPicked} but serial requires qty 1.`,
                });
            }
        }
        return errors;
    }

    isLotExpired(lotId) {
        return this.state.isLotExpired(lotId);
    }

    getTracking(productId) {
        return this.state.indexes.trackingByProductId[productId] || "none";
    }
}

export const barcodeScannerSyncService = {
    dependencies: ["orm", "barcodeScannerState"],
    start(env, {orm, barcodeScannerState}) {
        return new BarcodeScannerSync(orm, barcodeScannerState);
    },
};

registry.category("services").add("barcodeScannerSync", barcodeScannerSyncService);
