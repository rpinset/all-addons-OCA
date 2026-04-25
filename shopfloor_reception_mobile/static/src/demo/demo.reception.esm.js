/**
 * Copyright 2022 Camptocamp SA (http://www.camptocamp.com)
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
 */

import {demotools} from "/shopfloor_mobile_base/static/src/demo/demo.core.esm.js";

const move_by_id = {};
const move_line_by_id = {};
const move_line_by_move_id = {};
const make_reception_picking = () => {
    const picking = demotools.makePicking({}, {no_lines: true});
    picking.moves = [];
    picking.move_lines = [];
    for (let i = 0; i < 3; i++) {
        const move = demotools.makeMove();
        if (i === 0) {
            // Lead to set_lot on scan
            move.lot = undefined;
            move.product.display_name += " (lot required)";
        }
        picking.moves.push(move);
        move_by_id[move.id] = move;
        move_by_id[move.id].picking = {id: picking.id, name: picking.name};
        const ml = demotools.makeMoveLine();
        picking.move_lines.push(ml);
        move_line_by_id[ml.id] = ml;
        move_line_by_move_id[move.id] = ml;
        move_line_by_id[ml.id].picking = {id: picking.id, name: picking.name};
    }
    return picking;
};

const receipt_pickings = [];
for (let i = 0; i < 6; i++) {
    receipt_pickings.push(make_reception_picking());
}

const data_for_start = {
    next_state: "select_document",
    data: {
        start: {
            pickings: receipt_pickings,
        },
    },
};
const data_for_select_document = {
    next_state: "select_document",
    data: {
        select_document: {
            pickings: receipt_pickings,
        },
    },
};

/* eslint-disable no-unused-vars */
const DEMO_RECEPTION = {
    _data: {
        move_by_id,
        move_line_by_id,
        move_line_by_move_id,
    },
    start: data_for_start,
    list_stock_pickings: {
        next_state: "manual_selection",
        message: null,
        data: {
            manual_selection: {
                pickings: _.sampleSize(receipt_pickings, _.random(8)),
            },
        },
    },
    scan_line: function (data) {
        const move = _.find(Object.values(move_by_id), (x) => {
            return x.product.barcode === data.barcode;
        });
        const selected_move_line = move_line_by_move_id[move.id];
        if (_.isUndefined(move.lot)) {
            return {
                next_state: "set_lot",
                data: {
                    set_lot: {
                        picking: move.picking,
                        selected_move_line: [selected_move_line],
                    },
                },
            };
        }
        return {
            next_state: "set_packaging_dimension",
            data: {
                set_packaging_dimension: {
                    picking: move.picking,
                    selected_move_line: selected_move_line,
                    packaging: move.product.packaging[0],
                },
            },
        };
    },
    set_lot: function (data) {
        const line = move_line_by_id[data.selected_line_id];
        const lot = demotools.makeLot(
            {},
            {name: data.lot_name, expiration_date: data.expiration_date}
        );
        line.lot = lot;
        return {
            next_state: "set_lot",
            data: {
                set_lot: {
                    picking: line.picking,
                    selected_move_line: [line],
                },
            },
        };
    },
    set_lot_confirm_action: function (data) {
        const line = move_line_by_id[data.selected_line_id];
        return {
            next_state: "set_quantity",
            data: {
                set_quantity: {
                    picking: line.picking,
                    selected_move_line: [line],
                },
            },
        };
    },

    scan_document: function (data) {
        return {
            next_state: "select_move",
            data: {
                select_move: {
                    picking: receipt_pickings.find((p) => p.name === data.barcode),
                },
            },
        };
    },
    manual_select_move: function (data) {
        const move = move_by_id[data.move_id];
        const picking = move.picking;
        const line = move_line_by_move_id[move.id];
        return {
            next_state: "set_quantity",
            data: {
                set_quantity: {
                    picking: picking,
                    selected_move_line: [line],
                },
            },
        };
    },
    set_quantity: function (data) {
        const line = move_line_by_id[data.selected_line_id];
        return {
            next_state: "set_destination",
            data: {
                set_destination: {
                    selected_move_line: [line],
                    picking: line.picking,
                },
            },
        };
    },
    set_destination: function (data) {
        const res = data_for_select_document;
        res.data.message = "Transfer done";
        return res;
    },
};

const menuitem_id = demotools.addAppMenu(
    {
        name: "Reception",
        scenario: "reception",
        picking_types: [{id: 27, name: "Random type"}],
    },
    "re_1"
);
demotools.add_case("reception", menuitem_id, DEMO_RECEPTION);
