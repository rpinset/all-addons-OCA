1. In Sifende, create an API key for the right environment (Sandbox, Test or Production).
2. In *Facturación electrónica > Conectores*, create a connector with provider **Sifende**. Only
   one connector per company is allowed.
3. Choose the connector environment (*Pruebas* or *Producción*), paste the API key and, if you
   use your own Sifende deployment, change the base URL (HTTPS; HTTP is only accepted for
   `localhost`). Only administrators (*Ajustes*) can see and edit the API key and the base
   URL, because the URL decides where the key is sent.
4. Click **Probar Conexión**. It fails if the connector environment does not match the API key
   (`sk_live_` is *Producción*; `sk_sandbox_` and `sk_test_` are *Pruebas*; the match is also checked
   when saving the connector and before sending, cancelling or voiding), and it warns when the
   timbrado, establishment or expedition point used in Odoo do not exist in Sifende.
5. Load the same timbrado in Sifende. An expedition point used only by Odoo is recommended:
   Sifende accepts the document number Odoo sends and rejects numbers already in use.
6. Optional: in *Inventario > Configuración > Unidades de medida*, set the *Código de unidad de medida SIFEN* of each unit (77, unit, by default).
7. Optional but recommended: click **Registrar webhook** so that Sifende notifies Odoo as soon
   as SIFEN answers, without waiting for the cron. Odoo must be reachable from the Internet
   over HTTPS, and its base URL (`web.base.url`, in *Ajustes > Técnico > Parámetros del sistema*) must be the public one: Sifende rejects `http` and local addresses. The button
   registers `<web.base.url>/l10n_py_edi_sifende/webhook/<connector id>` for the
   `documento.aprobado`, `documento.rechazado` and `documento.cancelado` events and stores the
   signing secret, visible only to administrators. If the URL was already registered in
   Sifende, the button says so and **Rotar secreto** gets a new secret. If the webhook no
   longer exists in Sifende, **Rotar secreto** forgets it and warns you: click **Registrar webhook** again. **Quitar webhook** deletes it in Sifende. Each notification only triggers a
   poll of the current state in Sifende, so a late notification never overwrites the real
   state. The cron stays active as a fallback.
8. With several databases on the same server, the public URL must resolve to the right
   database (`dbfilter` or the subdomain), because Sifende does not send the database name.
9. Access rights. Each connector is only used from its own company. Sending, retrying and
   cancelling a document require *Contabilidad > Facturación* and write access to the document;
   checking its status also works for read-only users. *Inutilizar números* and **Test
   Connection** require *Contabilidad > Administrador*. The API key, the base URL and the
   webhook require *Ajustes*. Delivery note transports, with their vehicles and deliveries,
   belong to the company of their document: other companies can neither see nor edit them, and
   a transport without a document yet can only be edited by its creator.
