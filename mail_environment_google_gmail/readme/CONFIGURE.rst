Example of config file ::

  [ir.config_parameter]
  google_gmail_client_id = YOUR_GMAIL_API_CLIENT_ID
  google_gmail_client_secret = YOUR_GMAIL_API_CLIENT_SECRET

  [outgoing_mail.gmail_smtp_server]
  smtp_host = smtp.gmail.com
  smtp_port = 587
  smtp_user = example@gmail.com
  smtp_encryption = starttls
  smtp_authentication = gmail
  google_gmail_authorization_code = YOUR_ACCOUNT_AUTH_CODE
  google_gmail_refresh_token = YOUR_REFRESH_TOKEN

  [incoming_mail.gmail_imap_server]
  server_type = gmail
  smtp_host = imap.gmail.com
  smtp_port = 993
  user = example@gmail.com
  is_ssl = 1
  google_gmail_authorization_code = YOUR_ACCOUNT_AUTH_CODE
  google_gmail_refresh_token = YOUR_REFRESH_TOKEN


These two are global parameters, in core they're configured in General Settings:

* `YOUR_GMAIL_API_CLIENT_ID`: The client ID of your Google API project.
* `YOUR_GMAIL_API_CLIENT_SECRET`: The client secret of your Google API project.

These two are account-specific parameters:

* `YOUR_ACCOUNT_AUTH_CODE`: In core, there's a button that opens an URL to generate it.
* `YOUR_REFRESH_TOKEN`: In core, it's generated automatically when the
  `google_gmail_authorization_code` is written. It's not shown on the form, but I recommend
  having Odoo generate it and extract it from there, before setting up the server-env.
