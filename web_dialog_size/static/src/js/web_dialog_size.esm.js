/** @odoo-module **/

import {ActionDialog} from "@web/webclient/actions/action_dialog";
import {patch} from "@web/core/utils/patch";
import rpc from "web.rpc";
import {Component, onWillRender} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";
import {SelectCreateDialog} from "@web/views/view_dialogs/select_create_dialog";

export class ExpandButton extends Component {
    setup() {
        this.lastSize = this.currentSize = this.props.getsize();
        this.sizeRestored = false;
        this.config = rpc.query({
            model: "ir.config_parameter",
            method: "get_web_dialog_size_config",
        });

        onWillRender(() => {
            var self = this;
            // If the form lost its current state, we need to set it again
            if (this.props.getsize() !== this.currentSize) {
                this.props.setsize(this.currentSize);
            }
            // Check if we already are in full screen or if the form was restored.
            // If so we don't need to check the default maximize
            if (this.props.getsize() !== "dialog_full_screen" && !this.sizeRestored) {
                this.config.then(function (r) {
                    if (r.default_maximize && stop) {
                        self.dialog_button_extend();
                    }
                });
            }
        });
    }

    dialog_button_extend() {
        this.lastSize = this.props.getsize();
        this.props.setsize("dialog_full_screen");
        this.currentSize = "dialog_full_screen";
        this.sizeRestored = false;
        this.render();
    }

    dialog_button_restore() {
        this.props.setsize(this.lastSize);
        this.currentSize = this.lastSize;
        this.sizeRestored = true;
        this.render();
    }
}

ExpandButton.template = "web_dialog_size.ExpandButton";

patch(Dialog.prototype, "web_dialog_size.Dialog", {
    setup() {
        this._super(...arguments);
        this.setSize = this.setSize.bind(this);
        this.getSize = this.getSize.bind(this);
    },

    setSize(size) {
        this.props.size = size;
        this.render();
    },

    getSize() {
        return this.props.size;
    },
});

patch(SelectCreateDialog.prototype, "web_dialog_size.SelectCreateDialog", {
    setup() {
        this._super(...arguments);
        this.setSize = this.setSize.bind(this);
        this.getSize = this.getSize.bind(this);
    },

    setSize(size) {
        this.props.size = size;
        this.render();
    },

    getSize() {
        return this.props.size;
    },
});

Object.assign(ActionDialog.components, {ExpandButton});
SelectCreateDialog.components = Object.assign(SelectCreateDialog.components || {}, {
    ExpandButton,
});
Dialog.components = Object.assign(Dialog.components || {}, {ExpandButton});
// Patch annoying validation method
Dialog.props.size.validate = (s) =>
    ["sm", "md", "lg", "xl", "dialog_full_screen"].includes(s);
