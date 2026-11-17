import {defineModels, fields, models, mountView} from "@web/../tests/web_test_helpers";
import {describe, expect, test} from "@odoo/hoot";
import {defineMailModels} from "@mail/../tests/mail_test_helpers";

describe.current.tags("desktop");

class Partner extends models.Model {
    name = fields.Char();

    _records = [
        {id: 1, name: "Alice"},
        {id: 2, name: "Bob"},
    ];
}

class TierReview extends models.Model {
    _name = "tier.review";

    res_id = fields.Many2one({relation: "document"});
    sequence = fields.Integer();
    name = fields.Char();
    status = fields.Char();
    display_status = fields.Char();
    todo_by = fields.Char();
    reviewed_formated_date = fields.Char();
    comment = fields.Char();
    requested_by = fields.Many2one({relation: "partner"});
    done_by = fields.Many2one({relation: "partner"});

    _records = [
        {
            id: 1,
            res_id: 1,
            sequence: 10,
            name: "Manager",
            status: "forwarded",
            display_status: "Forwarded",
            requested_by: 1,
            done_by: 2,
        },
        {
            id: 2,
            res_id: 1,
            sequence: 11,
            name: "Forwarded to Alice",
            status: "pending",
            display_status: "Pending",
            todo_by: "Alice",
            requested_by: 2,
        },
    ];
}

class Document extends models.Model {
    review_ids = fields.One2many({relation: "tier.review", relation_field: "res_id"});

    _records = [{id: 1, review_ids: [1, 2]}];
}

defineMailModels();
defineModels([Partner, TierReview, Document]);

test("forwarded review: highlighted, requesters in a column", async () => {
    await mountView({
        type: "form",
        resModel: "document",
        resId: 1,
        arch: `<form><field name="review_ids" widget="tier_validation"/></form>`,
    });
    expect(".o_tier_review_body tbody tr:first").toHaveClass("alert-warning");
    expect(".o_tier_review_body tbody tr:last").not.toHaveClass("alert-warning");
    expect(".o_tier_review_requester").toHaveCount(0);
    expect("td[name=td_requested_by]").toHaveCount(2);
});
