/**
 * Copyright 2022 Camptocamp SA (http://www.camptocamp.com)
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
 */

import {demotools} from "/shopfloor_mobile_base/static/src/demo/demo.core.esm.js";

const reception_case = demotools.get_case("reception", "re_1");

const DEMO_RECEPTION_PKG = {
    ...reception_case,
    ...{
        scan_line: function (data) {
            const move = _.find(Object.values(reception_case._data.move_by_id), (x) => {
                return x.product.barcode === data.barcode;
            });
            const selected_move_line =
                reception_case._data.move_line_by_move_id[move.id];
            const packaging = selected_move_line.product.packaging[0];
            return {
                next_state: "set_packaging_dimension",
                data: {
                    set_packaging_dimension: {
                        picking: move.picking,
                        selected_move_line: selected_move_line,
                        packaging: packaging,
                    },
                },
            };
        },
        set_packaging_dimension: function (data) {
            const line = reception_case._data.move_line_by_id[data.selected_line_id];
            const picking = line.picking;
            return {
                // TODO: return to set_packaging_dimension if there's still pkg to set dimensions for
                next_state: "set_quantity",
                data: {
                    set_quantity: {
                        picking: picking,
                        selected_move_line: [line],
                    },
                },
            };
        },
    },
};

const menuitem_id = demotools.addAppMenu(
    {
        name: "Reception pkg dimension",
        scenario: "reception",
        picking_types: [{id: 27, name: "Random type"}],
    },
    "re_2"
);
demotools.add_case("reception", menuitem_id, DEMO_RECEPTION_PKG);
