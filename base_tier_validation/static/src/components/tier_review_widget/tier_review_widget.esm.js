import {Component} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";

export class ReviewsTable extends Component {
    _getReviewData() {
        const records = this.props.record.data.review_ids.records;
        return records.map((record) => record.data);
    }

    /** Hide the Comment column on documents where nobody commented. */
    get hasComments() {
        return this._getReviewData().some((review) => review.comment);
    }

    /**
     * The requester when every review has the same one, as after a single
     * validation request. Shown once above the table instead of a column.
     * Forwarding adds reviews requested by someone else: then the column
     * is kept.
     */
    get singleRequester() {
        const requesters = this._getReviewData().map((review) => review.requested_by);
        const first = requesters[0];
        if (!first || !first.id || requesters.some((r) => !r || r.id !== first.id)) {
            return null;
        }
        return first.display_name;
    }
}

ReviewsTable.template = "base_tier_validation.Collapse";
ReviewsTable.props = {...standardFieldProps};

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
