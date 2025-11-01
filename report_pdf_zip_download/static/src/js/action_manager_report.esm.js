// © 2017 Creu Blanca
// Copyright 2024 Quartile (https://www.quartile.co)
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
/* global URLSearchParams */
import {download} from "@web/core/network/download";
import {registry} from "@web/core/registry";
import {user} from "@web/core/user";

registry
    .category("ir.actions.report handlers")
    .add("zip_handler", async (action, options, env) => {
        const {report_type, report_name, zip_download, data} = action;
        const ctx = {...(user?.context || {}), ...(action?.context || {})};
        if (
            !(ctx.active_ids?.length > 1 && report_type === "qweb-pdf" && zip_download)
        ) {
            return false;
        }
        let url = `/report/zip/${encodeURIComponent(report_name)}`;
        const params = new URLSearchParams({context: JSON.stringify(ctx)});
        if (data && Object.keys(data).length) {
            params.set("options", JSON.stringify(data));
        } else if (ctx.active_ids?.length) {
            url += `/${ctx.active_ids.join(",")}`;
        }
        url += `?${params.toString()}`;
        const {ui, action: actionService} = env.services;
        ui.block();
        try {
            await download({
                url,
                data: {
                    data: JSON.stringify([url, "zip"]),
                    context: JSON.stringify(ctx),
                },
            });
        } finally {
            ui.unblock();
        }
        const {onClose} = options;
        if (action.close_on_report_download) {
            return actionService.doAction(
                {type: "ir.actions.act_window_close"},
                {onClose}
            );
        }
        onClose?.();
        return true;
    });
