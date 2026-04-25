env = locals().get("env")
# new message in employee channel
env.ref("mail.channel_all_employees").message_post(
    body="test",
    subject="This message should become demo's new_message_separator",
)
env.cr.commit()
