/* Copyright 2024 Hunki Enterprises BV
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
odoo.define("pos_container_deposit.components", function (require) {
    "use strict";

    const Orderline = require("point_of_sale.Orderline");
    const Registries = require("point_of_sale.Registries");
    const PosDepositOrderlineExtension = (Orderline) =>
        class PosDepositOrderline extends Orderline {
            selectLine() {
                /**
                 * Don't allow selecting deposit products
                 **/
                if (!this.props.line.is_container_deposit) {
                    super.selectLine(...arguments);
                }
            }
        };

    Registries.Component.extend(Orderline, PosDepositOrderlineExtension);
});
