/** @odoo-module **/

import {describe, expect, test} from "@odoo/hoot";
import {errorMessage} from "@barcode_scanner/js/api.esm";

describe("BarcodeScanner", () => {
    test("shows the server message for user-facing exceptions", () => {
        for (const name of [
            "odoo.exceptions.UserError",
            "odoo.exceptions.ValidationError",
            "odoo.exceptions.AccessError",
            "odoo.exceptions.MissingError",
        ]) {
            expect(
                errorMessage({data: {name, message: "Not enough stock."}}, "fallback")
            ).toBe("Not enough stock.");
        }
    });

    test("falls back for internal errors, without leaking the traceback", () => {
        expect(
            errorMessage(
                {
                    message: "Odoo Server Error",
                    data: {
                        name: "builtins.ValueError",
                        message: "bad value",
                        debug: "Traceback (most recent call last): ...",
                    },
                },
                "fallback"
            )
        ).toBe("fallback");
    });

    test("falls back for AccessDenied, without leaking auth detail", () => {
        expect(
            errorMessage(
                {
                    data: {
                        name: "odoo.exceptions.AccessDenied",
                        message: "Session expired",
                    },
                },
                "fallback"
            )
        ).toBe("fallback");
    });

    test("falls back when the envelope is missing or the message is empty", () => {
        expect(errorMessage(null, "fallback")).toBe("fallback");
        expect(errorMessage({}, "fallback")).toBe("fallback");
        expect(
            errorMessage(
                {data: {name: "odoo.exceptions.UserError", message: ""}},
                "fallback"
            )
        ).toBe("fallback");
        expect(
            errorMessage({data: {name: "odoo.exceptions.UserError"}}, "fallback")
        ).toBe("fallback");
    });
});
