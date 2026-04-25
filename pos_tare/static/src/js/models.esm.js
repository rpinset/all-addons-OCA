/** @odoo-module **/

import {convert_mass, format_tare} from "./tools.esm";
import {Model} from "point_of_sale.Registries";
import {Orderline} from "point_of_sale.models";
import field_utils from "web.field_utils";

const TareOrderline = (Orderline_) =>
    class extends Orderline_ {
        // /////////////////////////////
        // Overload Section
        // /////////////////////////////
        constructor(obj, options) {
            super(obj, options);
            if (options.json) {
                // The object has already been initialized by a call to
                // .init_from_JSON() in the parent's constructor.
                return;
            }
            this.tare = 0;
        }

        init_from_JSON(json) {
            super.init_from_JSON(json);
            this.tare = json.tare || 0;
        }

        clone() {
            const order_line = super.clone();
            order_line.tare = this.tare;
            return order_line;
        }

        export_as_JSON() {
            const json = super.export_as_JSON();
            json.tare = this.get_tare();
            return json;
        }

        export_for_printing() {
            const order_line = super.export_for_printing(...arguments);
            order_line.tare_quantity = this.get_tare();
            order_line.gross_quantity = this.get_gross_weight();
            return order_line;
        }

        // /////////////////////////////
        // Custom Section
        // /////////////////////////////
        set_tare(quantity, update_net_weight) {
            this.order.assert_editable();

            // Prevent to apply multiple times a tare to the same product.
            if (this.get_tare() > 0) {
                // This is valid because the tare is stored using product UOM.
                this.set_quantity(this.get_quantity() + this.get_tare());
                this.reset_tare();
            }

            if (quantity === "remove") {
                return;
            }

            // We convert the tare that is always measured in the same UoM into
            // the unit of measure for this order line.
            const tare_uom = this.pos.config.iface_tare_uom_id[0];
            const tare_unit = this.pos.units_by_id[tare_uom];
            // Same code as in Orderline.set_quantity(), to correctly handle
            // different decimal separators and values that have already be
            // converted from string to number.
            const tare =
                typeof quantity === "number"
                    ? quantity
                    : field_utils.parse.float(String(quantity ? quantity : 0));
            const line_unit = this.get_unit();
            // This will throw an exception if the UoM categories don't match.
            const tare_in_product_uom = convert_mass(tare, tare_unit, line_unit);
            if (update_net_weight) {
                const net_quantity = this.get_quantity() - tare_in_product_uom;
                // Update the quantity with the new weight net of tare quantity.
                this.set_quantity(net_quantity);
            }
            // Update tare value.
            this.tare = tare_in_product_uom;
        }

        reset_tare() {
            this.tare = 0;
        }

        get_tare() {
            return this.tare;
        }

        get_gross_weight() {
            return this.get_tare() + this.get_quantity();
        }

        get_tare_str_with_unit() {
            const unit = this.get_unit();
            const tare_str = format_tare(this.pos, this.tare, this.get_unit());
            return tare_str + " " + unit.name;
        }

        get_gross_weight_str_with_unit() {
            const unit = this.get_unit();
            const gross_weight_str = format_tare(
                this.pos,
                this.get_gross_weight(),
                this.get_unit()
            );
            return gross_weight_str + " " + unit.name;
        }
    };

Model.extend(Orderline, TareOrderline);
