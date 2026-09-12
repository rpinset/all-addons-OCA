import {registry} from "@web/core/registry";
import {_t} from "@web/core/l10n/translation";

// Server exceptions whose message is safe to show to operators. Anything
// else (real internal errors) falls back to a generic message so the PDA
// never displays raw Python tracebacks (which the RPC layer puts in
// error.data.debug, never read here).
// MissingError is included because the record is gone (operator can reload).
// AccessDenied is excluded because it signals authentication/session failure
// (generic message plus login flow, no raw detail).
const USER_ERROR_NAMES = new Set([
    "odoo.exceptions.UserError",
    "odoo.exceptions.ValidationError",
    "odoo.exceptions.AccessError",
    "odoo.exceptions.MissingError",
]);

export function errorMessage(error, fallback) {
    const message = error?.data?.message;
    return USER_ERROR_NAMES.has(error?.data?.name) &&
        typeof message === "string" &&
        message
        ? message
        : fallback;
}

export const barcodeApiService = {
    dependencies: ["orm", "notification", "dialog"],
    start(env, {orm, notification, dialog}) {
        return {
            async call(model, method, args = [], kwargs = {}) {
                try {
                    return await orm.call(model, method, args, kwargs);
                } catch (error) {
                    const message = errorMessage(
                        error,
                        _t("An error occurred while calling the server.")
                    );
                    notification.add(message, {type: "danger"});
                    throw error;
                }
            },

            async searchRead(model, domain, fields, options = {}) {
                try {
                    return await orm.searchRead(model, domain, fields, options);
                } catch (error) {
                    const message = errorMessage(
                        error,
                        _t("An error occurred while fetching data.")
                    );
                    notification.add(message, {type: "danger"});
                    throw error;
                }
            },

            async readGroup(model, domain, fields, groupby, options = {}) {
                try {
                    return await orm.readGroup(model, domain, fields, groupby, options);
                } catch (error) {
                    const message = errorMessage(
                        error,
                        _t("An error occurred while grouping data.")
                    );
                    notification.add(message, {type: "danger"});
                    throw error;
                }
            },

            async read(model, ids, fields) {
                try {
                    return await orm.read(model, ids, fields);
                } catch (error) {
                    const message = errorMessage(
                        error,
                        _t("An error occurred while reading records.")
                    );
                    notification.add(message, {type: "danger"});
                    throw error;
                }
            },

            async write(model, ids, data) {
                try {
                    return await orm.write(model, ids, data);
                } catch (error) {
                    const message = errorMessage(
                        error,
                        _t("An error occurred while saving records.")
                    );
                    notification.add(message, {type: "danger"});
                    throw error;
                }
            },

            async create(model, data) {
                try {
                    return await orm.create(model, data);
                } catch (error) {
                    const message = errorMessage(
                        error,
                        _t("An error occurred while creating records.")
                    );
                    notification.add(message, {type: "danger"});
                    throw error;
                }
            },

            async unlink(model, ids) {
                try {
                    return await orm.unlink(model, ids);
                } catch (error) {
                    const message = errorMessage(
                        error,
                        _t("An error occurred while deleting records.")
                    );
                    notification.add(message, {type: "danger"});
                    throw error;
                }
            },

            notify(message, options = {}) {
                notification.add(message, options);
            },

            openDialog(dialogClass, props = {}) {
                dialog.add(dialogClass, props);
            },
        };
    },
};

registry.category("services").add("barcodeApi", barcodeApiService);
