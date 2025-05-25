/** @odoo-module **/

import Dialog from "web.Dialog";
import {Component, onMounted, onWillStart, useState, useSubEnv} from "@odoo/owl";
import {DatePicker} from "@web/core/datepicker/datepicker";
import {FilterMenu} from "@web/search/filter_menu/filter_menu";
import {SearchBar} from "@web/search/search_bar/search_bar";
import {SearchModel} from "@web/search/search_model";
import {parseDate} from "@web/core/l10n/dates";
import {qweb} from "web.core";
import {registry} from "@web/core/registry";
import {useBus, useService} from "@web/core/utils/hooks";

export class MisReportWidget extends Component {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.user = useService("user");
        this.action = useService("action");
        this.view = useService("view");
        this.JSON = JSON;
        this.state = useState({
            mis_report_data: {header: [], body: [], notes: {}},
            pivot_date: null,
            can_edit_annotation: false,
            can_read_annotation: false,
        });
        this.searchModel = new SearchModel(this.env, {
            user: this.user,
            orm: this.orm,
            view: this.view,
        });
        useSubEnv({searchModel: this.searchModel});
        useBus(this.env.searchModel, "update", async () => {
            await this.env.searchModel.sectionsPromise;
            this.refresh();
        });
        onWillStart(this.willStart);

        onMounted(this._onMounted);
    }

    // Lifecycle
    async willStart() {
        const [result] = await this.orm.read(
            "mis.report.instance",
            [this._instanceId()],
            [
                "source_aml_model_name",
                "widget_show_filters",
                "widget_show_settings_button",
                "widget_search_view_id",
                "pivot_date",
                "widget_show_pivot_date",
                "user_can_read_annotation",
                "user_can_edit_annotation",
                "wide_display_by_default",
            ],
            {context: this.context}
        );
        this.source_aml_model_name = result.source_aml_model_name;
        this.widget_show_filters = result.widget_show_filters;
        this.widget_show_settings_button = result.widget_show_settings_button;
        this.widget_search_view_id =
            result.widget_search_view_id && result.widget_search_view_id[0];
        this.state.pivot_date = parseDate(result.pivot_date);
        this.widget_show_pivot_date = result.widget_show_pivot_date;
        if (this.showSearchBar) {
            // Initialize the search model
            await this.searchModel.load({
                resModel: this.source_aml_model_name,
                searchViewId: this.widget_search_view_id,
            });
        }

        this.wide_display = result.wide_display_by_default;

        // Compute the report
        this.refresh();
        this.state.can_edit_annotation = result.user_can_edit_annotation;
        this.state.can_read_annotation = result.user_can_read_annotation;
    }

    async _onMounted() {
        this.resize_sheet();
    }

    get showSearchBar() {
        return (
            this.source_aml_model_name &&
            this.widget_show_filters &&
            this.widget_search_view_id
        );
    }

    get showPivotDate() {
        return this.widget_show_pivot_date;
    }

    /**
     * Return the id of the mis.report.instance to which the widget is
     * bound.
     *
     * @returns int
     */
    _instanceId() {
        if (this.props.value) {
            return this.props.value;
        }

        /*
         * This trick is needed because in a dashboard the view does
         * not seem to be bound to an instance: it seems to be a limitation
         * of Odoo dashboards that are not designed to contain forms but
         * rather tree views or charts.
         */
        var context = this.props.record.context;
        if (context.active_model === "mis.report.instance") {
            return context.active_id;
        }
    }

    get context() {
        var ctx = super.context;
        if (this.showSearchBar) {
            ctx = {
                ...ctx,
                mis_analytic_domain: this.searchModel.searchDomain,
            };
        }
        if (this.showPivotDate && this.state.pivot_date) {
            ctx = {
                ...ctx,
                mis_pivot_date: this.state.pivot_date,
            };
        }
        return ctx;
    }

    async drilldown(event) {
        const drilldown = JSON.parse(event.target.dataset.drilldown);
        const action = await this.orm.call(
            "mis.report.instance",
            "drilldown",
            [this._instanceId(), drilldown],
            {context: this.context}
        );
        this.action.doAction(action);
    }

    async refresh() {
        this.state.mis_report_data = await this.orm.call(
            "mis.report.instance",
            "compute",
            [this._instanceId()],
            {context: this.context}
        );
    }

    async refresh_annotation() {
        this.state.mis_report_data.notes = await this.orm.call(
            "mis.report.instance",
            "get_notes_by_cell_id",
            [this._instanceId()],
            {context: this.context}
        );
    }

    async printPdf() {
        const action = await this.orm.call(
            "mis.report.instance",
            "print_pdf",
            [this._instanceId()],
            {context: this.context}
        );
        this.action.doAction(action);
    }

    async exportXls() {
        const action = await this.orm.call(
            "mis.report.instance",
            "export_xls",
            [this._instanceId()],
            {context: this.context}
        );
        this.action.doAction(action);
    }

    async displaySettings() {
        const action = await this.orm.call(
            "mis.report.instance",
            "display_settings",
            [this._instanceId()],
            {context: this.context}
        );
        this.action.doAction(action);
    }

    async _remove_annotation(cell_id) {
        await this.orm.call(
            "mis.report.instance.annotation",
            "remove_annotation",
            [cell_id, this._instanceId()],
            {context: this.context}
        );
        this.refresh_annotation();
    }

    async _save_annotation(cell_id) {
        const text = document.querySelector(".o_mis_builder_annotation_text").value;
        await this.orm.call(
            "mis.report.instance.annotation",
            "set_annotation",
            [cell_id, this._instanceId(), text],
            {context: this.context}
        );
        await this.refresh_annotation();
    }

    async annotate(event) {
        const cell_id = event.target.dataset.cellId;
        const note = this.state.mis_report_data.notes[cell_id];
        const note_text = (note && note.text) || "";
        var buttons = [
            {
                text: this.env._t("Save"),
                classes: "btn-primary",
                close: true,
                click: this._save_annotation.bind(this, cell_id),
            },
            {
                text: this.env._t("Cancel"),
                close: true,
            },
        ];
        if (typeof note !== "undefined") {
            buttons.push({
                text: this.env._t("Remove"),
                classes: "btn-secondary",
                close: true,
                click: this._remove_annotation.bind(this, cell_id),
            });
        }

        new Dialog(this, {
            title: "Annotate",
            size: "medium",
            $content: $(
                qweb.render("mis_builder.annotation_dialog", {
                    text: note_text,
                })
            ),
            buttons: buttons,
        }).open();
    }

    async remove_annotation(event) {
        const cell_id = event.target.dataset.cellId;
        this._remove_annotation(cell_id);
    }

    onDateTimeChanged(ev) {
        this.state.pivot_date = ev;
        this.refresh();
    }

    async toggle_wide_display() {
        this.wide_display = !this.wide_display;
        this.resize_sheet();
    }

    async resize_sheet() {
        var sheet_element = document.getElementsByClassName("o_form_sheet")[0];
        sheet_element.classList.toggle(
            "oe_mis_builder_report_wide_sheet",
            this.wide_display
        );
        var button_resize_element = document.getElementById("icon_resize");
        button_resize_element.classList.toggle("fa-expand", !this.wide_display);
        button_resize_element.classList.toggle("fa-compress", this.wide_display);
    }
}

MisReportWidget.components = {FilterMenu, SearchBar, DatePicker};
MisReportWidget.template = "mis_builder.MisReportWidget";

registry.category("fields").add("mis_report_widget", MisReportWidget);
