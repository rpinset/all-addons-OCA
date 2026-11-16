import {describe, expect, test} from "@odoo/hoot";
import {BarcodeScannerFeedbackService} from "@barcode_scanner/js/services/feedback_service.esm";

function makeFeedback(notifications) {
    const feedback = new BarcodeScannerFeedbackService({
        add: (...args) => notifications.push(args),
    });
    feedback.enabled = {audio: false, vibration: false, flash: false};
    return feedback;
}

describe("BarcodeScannerFeedbackService", () => {
    test("error feedback uses the danger notification type", () => {
        const notifications = [];
        const feedback = makeFeedback(notifications);
        const message = "Unable to apply the cycle count";

        feedback.error({message, notify: true});

        expect(notifications).toEqual([[message, {type: "danger"}]]);
        feedback.destroy();
    });

    test("feedback levels map to valid Odoo notification types", () => {
        const cases = [
            ["success", "success"],
            ["warning", "warning"],
            ["info", "info"],
            ["error", "danger"],
        ];
        for (const [level, type] of cases) {
            const notifications = [];
            const feedback = makeFeedback(notifications);
            feedback[level]({message: level, notify: true});
            expect(notifications).toEqual([[level, {type}]]);
            feedback.destroy();
        }
    });
});
