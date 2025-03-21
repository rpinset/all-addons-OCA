odoo.define(
    "sale_planner_calendar.sale_planner_calendar_event_sales",
    function (require) {
        "use strict";
        var ListController = require("web.ListController");
        var ListView = require("web.ListView");

        var KanbanController = require("web.KanbanController");
        var KanbanRecord = require("web.KanbanRecord");
        var KanbanView = require("web.KanbanView");

        var viewRegistry = require("web.view_registry");
        var KanbanRenderer = require("web.KanbanRenderer");

        function renderViewNewSaleOrderButton() {
            if (this.$buttons) {
                var self = this;
                var calendar_summary_id =
                    self.initialState.getContext().default_calendar_summary_id;
                this._rpc({
                    model: "calendar.event",
                    method: "action_open_sale_order",
                    args: [false, {new_order: true}],
                    context: {calendar_summary_id: calendar_summary_id || false},
                }).then(function (action) {
                    self.$buttons.on("click", ".o_button_new_sale_order", function () {
                        self.do_action(action);
                    });
                });
            }
        }

        var SalePlannerCalendarEventListController = ListController.extend({
            willStart: function () {
                var self = this;
                var ready = this.getSession()
                    .user_has_group("sales_team.group_sale_salesman")
                    .then(function (is_sale_user) {
                        if (is_sale_user) {
                            self.buttons_template =
                                "SalePlannerCalendarEventListView.buttons";
                        }
                    });
                return Promise.all([this._super.apply(this, arguments), ready]);
            },
            renderButtons: function () {
                this._super.apply(this, arguments);
                renderViewNewSaleOrderButton.apply(this, arguments);
            },
        });

        var SalePlannerCalendarEventListView = ListView.extend({
            config: _.extend({}, ListView.prototype.config, {
                Controller: SalePlannerCalendarEventListController,
            }),
        });
        const SalePlannerCalendarEventKanbanRecord = KanbanRecord.extend({
            events: {
                ...KanbanRecord.prototype.events,
                "click .oe_planner_calendar_previous_after":
                    "_onSalePlannerCalendarKanbanButtonPreviousAfter",
                "click .oe_planner_calendar_set_time":
                    "_onSalePlannerCalendarKanbanButtonSetTime",
            },
            _onSalePlannerCalendarKanbanButtonPreviousAfter: function (ev) {
                var dataset = this.getParent().getChildren();
                var index = dataset.indexOf(this);
                var timeUnit = -this.recordData.duration;
                var base_item = {};
                if (ev.currentTarget.name === "button_move_to_previous") {
                    if (index === 0) {
                        return;
                    }
                    base_item = dataset[index - 1];
                } else {
                    if (index === dataset.length - 1) {
                        return;
                    }
                    base_item = dataset[index + 1];
                    timeUnit = base_item.recordData.duration;
                }
                this.trigger_up("field_changed", {
                    changes: {hour: base_item.recordData.hour + timeUnit},
                    dataPointID: this.db_id,
                    onSuccess: () => {
                        this.trigger_up("reload", {keepChanges: true});
                    },
                });
            },
            _onSalePlannerCalendarKanbanButtonSetTime: function () {
                this.do_action(
                    {
                        type: "ir.actions.act_window",
                        name: "Sale planner calendar change hour",
                        res_model: "calendar.event",
                        view_mode: "form",
                        views: [[false, "form"]],
                        context: {
                            form_view_ref:
                                "sale_planner_calendar.view_sale_planner_calendar_change_hour_form",
                        },
                        target: "new",
                        res_id: this.recordData.id,
                    },
                    {
                        on_close: () => {
                            this.trigger_up("reload", {keepChanges: true});
                        },
                    }
                );
            },
        });
        const SalePlannerCalendarEventKanbanRenderer = KanbanRenderer.extend({
            config: _.extend({}, KanbanRenderer.prototype.config, {
                KanbanRecord: SalePlannerCalendarEventKanbanRecord,
            }),
        });
        var SalePlannerCalendarEventKanbanController = KanbanController.extend({
            willStart: function () {
                var self = this;
                var ready = this.getSession()
                    .user_has_group("sales_team.group_sale_salesman")
                    .then(function (is_sale_user) {
                        if (is_sale_user) {
                            self.buttons_template =
                                "SalePlannerCalendarEventKanbanView.buttons";
                        }
                    });
                return Promise.all([this._super.apply(this, arguments), ready]);
            },
            renderButtons: function () {
                this._super.apply(this, arguments);
                renderViewNewSaleOrderButton.apply(this, arguments);
            },
        });

        var SalePlannerCalendarEventKanbanView = KanbanView.extend({
            config: _.extend({}, KanbanView.prototype.config, {
                Controller: SalePlannerCalendarEventKanbanController,
                Renderer: SalePlannerCalendarEventKanbanRenderer,
            }),
        });

        viewRegistry.add(
            "sale_planner_calendar_event_tree",
            SalePlannerCalendarEventListView
        );
        viewRegistry.add(
            "sale_planner_calendar_event_kanban",
            SalePlannerCalendarEventKanbanView
        );
    }
);
