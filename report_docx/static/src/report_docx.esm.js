/* @odoo-module */

import {download} from "@web/core/network/download";
import {registry} from "@web/core/registry";

registry
    .category("ir.actions.report handlers")
    .add("docx", async function (action, options, env) {
        if (action.report_type === "docx") {
            env.services.ui.block();
            const context = action.context || {};
            try {
                await download({
                    url: "/report_docx",
                    data: {
                        ids: JSON.stringify(context.active_ids || []),
                        context: JSON.stringify(
                            Object.assign({}, env.services.user.context, context)
                        ),
                        report_name: action.report_name,
                        data: JSON.stringify(action.data || {}),
                    },
                });
            } finally {
                env.services.ui.unblock();
            }
            const onClose = options.onClose;
            if (action.close_on_report_download) {
                return env.services.action.doAction(
                    {type: "ir.actions.act_window_close"},
                    {onClose}
                );
            } else if (onClose) {
                onClose();
            }
            return Promise.resolve(true);
        }
        return Promise.resolve(false);
    });
