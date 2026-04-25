env = locals().get("env")
# call sending wizard on some moves asynchronously
action = (
    env["account.move"]
    .search(
        [
            ("move_type", "=", "out_invoice"),
            ("state", "=", "posted"),
            ("company_id", "=", env.ref("base.main_company").id),
        ]
    )
    .action_send_and_print()
)
env[action["res_model"]].with_context(**action["context"]).create(
    {
        "checkbox_download": False,
    }
).action_send_and_print()
env.cr.commit()
