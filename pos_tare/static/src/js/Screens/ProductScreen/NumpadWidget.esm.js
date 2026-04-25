/** @odoo-module **/

import {Component} from "point_of_sale.Registries";
import NumpadWidget from "point_of_sale.NumpadWidget";

const TareNumpadWidget = (NumpadWidget_) =>
    class extends NumpadWidget_ {
        changeMode(mode) {
            if (mode === "tare") {
                this.trigger("set-numpad-mode", {mode});
                return;
            }
            super.changeMode(mode);
        }
    };

Component.extend(NumpadWidget, TareNumpadWidget);

export default NumpadWidget;
