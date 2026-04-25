/**
 * Copyright 2021 Camptocamp SA (http://www.camptocamp.com)
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

import {demotools} from "/shopfloor_mobile_base/static/src/demo/demo.core.esm.js";

const pick = demotools.makePicking();
const pack = demotools.makePack();
const shipment = {
    id: 1,
    name: "SA/OUT/0000001",
    state: "confirmed",
    dock: {
        id: 1,
        name: "Dock 01",
    },
};

const lading = [];
for (let i = 0; i < 5; i++) {
    lading.push(
        demotools.makePicking({
            load_state: _.sample(["all", "partial", "none"]),
            loaded_pickings_count: _.random(0, 5),
            loaded_packages_count: _.random(0, 5),
            total_packages_count: _.random(5, 10),
            loaded_bulk_lines_count: _.random(0, 5),
            total_bulk_lines_count: _.random(5, 10),
            loaded_weight: _.random(100, 500),
        })
    );
}

const on_dock = [];
for (let i = 0; i < 4; i++) {
    on_dock.push(
        demotools.makePicking({
            load_state: _.sample(["all", "partial", "none"]),
            loaded_pickings_count: _.random(0, 5),
            loaded_packages_count: _.random(0, 5),
            total_packages_count: _.random(5, 10),
            loaded_bulk_lines_count: _.random(0, 5),
            total_bulk_lines_count: _.random(5, 10),
            loaded_weight: _.random(100, 500),
        })
    );
}

const DELIVERY_SHIPMENT_CASE = {
    scan_dock: {
        next_state: "scan_document",
        data: {
            scan_document: {
                shipment_advice: _.cloneDeep(shipment),
            },
        },
    },
    scan_document: {
        OP1: {
            next_state: "scan_document",
            message: {
                message_type: "info",
                body: "Operation found",
            },
            data: {
                scan_document: {
                    picking: _.cloneDeep(pick),
                    shipment_advice: _.cloneDeep(shipment),
                },
            },
        },
        PACK1: {
            next_state: "scan_document",
            message: {
                message_type: "info",
                body: "Pack found",
            },
            data: {
                scan_document: {
                    shipment_advice: _.cloneDeep(shipment),
                    packaging: _.cloneDeep(pack),
                },
            },
        },
        next_state: "loading_list",
        data: {
            loading_list: {
                shipment_advice: _.cloneDeep(shipment),
                lading: lading,
                on_dock: on_dock,
            },
        },
    },
    loading_list: {
        next_state: "validate",
        data: {
            validate: {
                shipment_advice: _.cloneDeep(shipment),
                lading: lading[0],
                loaded_weight: 100,
                on_dock: on_dock,
            },
        },
    },
    // TODO: this should be improved to use real data from submitted request.
    validate: {
        next_state: "scan_dock",
        message: {
            message_type: "info",
            body: "Shipment ABC has been validated",
        },
        data: {
            scan_dock: {},
        },
    },
};

const menuitem_id = demotools.addAppMenu(
    {
        name: "Delivery shipment 1",
        scenario: "delivery_shipment",
        picking_types: [{id: 27, name: "Random type"}],
    },
    "delivery_shipment_1"
);

demotools.add_case("delivery_shipment", menuitem_id, DELIVERY_SHIPMENT_CASE);
