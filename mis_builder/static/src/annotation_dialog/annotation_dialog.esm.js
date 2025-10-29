/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";

export class AnnotationDialog extends Component {
    static components = {Dialog};
    static props = {
        close: Function,
        annotationText: {type: String, optional: true},
        confirm: {type: Function, optional: true},
        title: {type: String},
        remove: {type: Function, optional: true},
        canRemove: {type: Boolean},
    };
    static template = "mis_builder.AnnotationDialog";

    setup() {
        this.state = useState({
            annotationText: this.props.annotationText,
        });
    }

    confirm() {
        this.props.confirm(this.state.annotationText);
        this.props.close();
    }

    remove() {
        this.props.remove();
        this.props.close();
    }
}
