/** @odoo-module **/

import {registry} from "@web/core/registry";

import {useService} from "@web/core/utils/hooks";

const {Component} = owl;

export class ReviewsTable extends Component {
    setup() {
        this.collapse = false;
        this.orm = useService("orm");
        this.reviews = [];
    }
    _getReviewData() {
        const records = this.env.model.root.data.review_ids.records;
        const reviews = [];
        for (var i = 0; i < records.length; i++) {
            reviews.push(records[i].data);
        }
        return reviews;
    }
    onToggleCollapse(ev) {
        var $panelHeading = $(ev.currentTarget).closest(".panel-heading");
        if (this.collapse) {
            $panelHeading.next("div#collapse1").hide();
        } else {
            $panelHeading.next("div#collapse1").show();
        }
        this.collapse = !this.collapse;
    }
}

ReviewsTable.template = "base_tier_validation.Collapse";

export const reviewsTableComponent = {
    component: ReviewsTable,
    supportedTypes: ["one2many"],
    relatedFields: [
        {name: "id", type: "integer"},
        {name: "sequence", type: "integer"},
        {name: "name", type: "char"},
        {name: "display_status", type: "char"},
        {name: "todo_by", type: "char"},
        {name: "status", type: "char"},
        {name: "reviewed_formated_date", type: "char"},
        {name: "comment", type: "char"},
        {name: "requested_by", type: "many2one", relation: "partner"},
        {name: "done_by", type: "many2one", relation: "partner"},
    ],
};

registry.category("fields").add("form.tier_validation", reviewsTableComponent);
