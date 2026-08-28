1. In Mautic, go to *Settings > API Credentials* and create a new API
   credential using the *OAuth2* authorization method.
2. Go to *Connectors > Mautic Backends* in Odoo and create a new backend
   with the Mautic URL and the Client ID / Client Secret from step 1.
3. Copy the *Callback URL* shown on the backend form and paste it as the
   *Redirect URI* of the Mautic API credential (step 1). Save the Mautic
   credential.
4. Back in Odoo, click *Connect to Mautic*: you will be redirected to
   Mautic to authorize the application, then back to Odoo with the backend
   marked as *Connected*.
