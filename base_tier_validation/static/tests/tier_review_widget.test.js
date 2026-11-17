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
        // Document 1: one requester, no comments.
        {
            id: 1,
            res_id: 1,
            sequence: 10,
            name: "Manager",
            status: "approved",
            display_status: "Approved",
            requested_by: 1,
            done_by: 2,
        },
        {
            id: 2,
            res_id: 1,
            sequence: 20,
            name: "Director",
            status: "pending",
            display_status: "Pending",
            todo_by: "Bob",
            requested_by: 1,
        },
        // Document 2: one requester, one comment.
        {
            id: 3,
            res_id: 2,
            sequence: 10,
            name: "Manager",
            status: "rejected",
            display_status: "Rejected",
            requested_by: 1,
            done_by: 2,
            comment: "Too expensive",
        },
        // Document 3: two requesters.
        {
            id: 4,
            res_id: 3,
            sequence: 10,
            name: "Manager",
            status: "approved",
            display_status: "Approved",
            requested_by: 1,
            done_by: 2,
        },
        {
            id: 5,
            res_id: 3,
            sequence: 20,
            name: "Director",
            status: "pending",
            display_status: "Pending",
            todo_by: "Alice",
            requested_by: 2,
        },
    ];
}

class Document extends models.Model {
    review_ids = fields.One2many({relation: "tier.review", relation_field: "res_id"});

    _records = [
        {id: 1, review_ids: [1, 2]},
        {id: 2, review_ids: [3]},
        {id: 3, review_ids: [4, 5]},
    ];
}

defineMailModels();
defineModels([Partner, TierReview, Document]);

async function mountReviews(resId) {
    await mountView({
        type: "form",
        resModel: "document",
        resId,
        arch: `<form><field name="review_ids" widget="tier_validation"/></form>`,
    });
}

test("one requester: shown above the table, no column", async () => {
    await mountReviews(1);
    expect(".o_tier_review_requester").toHaveText("· requested by Alice");
    expect("th[name=th_requested_by]").toHaveCount(0);
    expect(".o_tier_review_body tbody tr").toHaveCount(2);
});

test("no comments: no Comment column", async () => {
    await mountReviews(1);
    expect("th[name=th_comment]").toHaveCount(0);
    expect("td[name=td_comment]").toHaveCount(0);
});

test("a comment: Comment column shown", async () => {
    await mountReviews(2);
    expect("th[name=th_comment]").toHaveCount(1);
    expect("td[name=td_comment]").toHaveText("Too expensive");
});

test("several requesters: Requested by column instead", async () => {
    await mountReviews(3);
    expect(".o_tier_review_requester").toHaveCount(0);
    expect("td[name=td_requested_by]").toHaveCount(2);
    expect("td[name=td_requested_by]:last").toHaveText("Bob");
});

test("status shown as a badge", async () => {
    await mountReviews(1);
    expect("tbody tr:first").toHaveClass("table-success");
    expect("tbody tr:first .badge").toHaveClass("text-bg-success");
    expect("tbody tr:last .badge").toHaveClass("text-bg-warning");
    expect("tbody tr:last .badge").toHaveText("Pending");
});
