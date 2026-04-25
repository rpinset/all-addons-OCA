import {ListRenderer} from "@web/views/list/list_renderer";
import {SaleOrderLineOne2Many} from "@sale/js/sale_order_line_field/sale_order_line_field";
import {patch} from "@web/core/utils/patch";

patch(ListRenderer.prototype, {
    get canCreate() {
        const parentRecord = this.props.list.model.root;
        const disableAddingLines = parentRecord?.data?.disable_adding_lines;
        return !disableAddingLines && super.canCreate;
    },
});

patch(SaleOrderLineOne2Many.prototype, {
    get displayControlPanelButtons() {
        const fieldName = this.props.name;
        if (this.props.viewMode === "kanban" && fieldName === "order_line") {
            const disabled = this.props.record?.data?.disable_adding_lines;
            return !disabled && super.displayControlPanelButtons;
        }
        return super.displayControlPanelButtons;
    },
});
