**English**

**Migration from l10n_it_declaration_of_intent (Odoo 16)**

If the module `l10n_it_declaration_of_intent` is installed, the migration runs
automatically when installing `l10n_it_edi_doi_extension`. No manual SQL or scripts
are required.

Prerequisites:

- Back up the database before starting
- The `openupgradelib` Python library must be installed in the Odoo environment

Steps:

1. **Back up the database.**

2. **Install the module:**

   The pre-init hook runs automatically and handles:

   - Renaming of the old table and model
   - Splitting `telematic_protocol` into `protocol_number_part1` / `protocol_number_part2`
   - Renaming fields (`date` → `issue_date`, `date_start` → `start_date`, etc.)
   - Mapping states (`valid` → `active`, `expired` → `terminated`, `close` → `revoked`)
   - Removing old views incompatible with Odoo 18

   The post-init hook:

   - Creates `account.move.doi` bridge records from the old many2many relations
   - Populates `l10n_it_edi_doi_amount` on invoices that had no DOI tax lines
   - Cleans up residual metadata from the old module and removes it entirely
     (records, model metadata, and module entry — no manual uninstall is needed
     or possible after this point)

3. **Verify the migrated data:**

   - Declarations appear in the new menu with correct protocol numbers
   - States are correctly mapped
   - Invoice links are working
   - Computed amounts (invoiced, remaining) are shown correctly
   - **For invoices that had multiple declarations in v16: check the**
     **"Declarations of Intent" tab and assign the correct amount to each entry**
     **(they are migrated with `amount = 0`)**

**Data that is NOT migrated** (no equivalent in v18):

- `partner_document_number`, `partner_document_date`
- `taxes_ids`, `fiscal_position_id`
- Declaration lines (`declaration_line` model)
- Yearly limits (`yearly_limit` model) — adjust individual declaration thresholds manually

**Troubleshooting:**

- *ValidationError about repartition lines during installation*: the migration script
  automatically adds missing repartition lines to split payment group taxes. If the
  error persists, check that `openupgradelib` is installed correctly.

- *Duplicate key error on fiscal positions or taxes during l10n_it_edi_doi installation*:
  this can happen when the old module had already created the same fiscal position data.
  The installation of `l10n_it_edi_doi` may fail or show a warning. Remove the duplicate
  fiscal position tax mappings manually and retry.

- *Invoice DOI amount shows 0 or an approximate value*: in the normal migration path,
  `l10n_it_edi_doi_amount` is derived from the sum of the v16 declaration line amounts
  (accurate). If the declaration lines table was already absent at migration time, the
  fallback uses `ABS(amount_untaxed)` as an approximation. If you see zero amounts,
  open each affected invoice and assign the correct amount in the "Declarations of
  Intent" tab.

- *Yearly limits not migrated*: the concept no longer exists in v18. Review each
  declaration and set the `threshold` field to the appropriate value.


**Italiano**

**Migrazione da l10n_it_declaration_of_intent (Odoo 16)**

Se il modulo `l10n_it_declaration_of_intent` è installato, la migrazione avviene
automaticamente durante l'installazione di `l10n_it_edi_doi_extension`. Non è
necessario eseguire script o SQL manualmente.

Prerequisiti:

- Eseguire un backup del database prima di iniziare
- La libreria Python `openupgradelib` deve essere installata nell'ambiente Odoo

Passi:

1. **Eseguire un backup del database.**

2. **Installare il modulo:**

   L'hook pre-init viene eseguito automaticamente e gestisce:

   - Rinomina della tabella e del modello
   - Split di `telematic_protocol` in `protocol_number_part1` / `protocol_number_part2`
   - Rinomina dei campi (`date` → `issue_date`, `date_start` → `start_date`, ecc.)
   - Mappatura degli stati (`valid` → `active`, `expired` → `terminated`, `close` → `revoked`)
   - Rimozione delle view del vecchio modulo incompatibili con Odoo 18

   L'hook post-init:

   - Crea i record bridge `account.move.doi` dalle vecchie relazioni many2many
   - Popola `l10n_it_edi_doi_amount` sulle fatture prive di righe con imposta DOI
   - Pulisce i metadati residui del vecchio modulo e lo rimuove completamente
     (record, metadati del modello e voce del modulo — non è necessaria né
     possibile una disinstallazione manuale)

3. **Verificare i dati migrati:**

   - Le dichiarazioni compaiono nel nuovo menu con i numeri di protocollo corretti
   - Gli stati sono correttamente mappati
   - I collegamenti alle fatture funzionano
   - Gli importi calcolati (fatturato, residuo) sono visualizzati correttamente
   - **Per le fatture che avevano più dichiarazioni in v16: controllare il tab**
     **"Dichiarazioni di Intento" e assegnare l'importo corretto a ciascuna voce**
     **(vengono migrate con `amount = 0`)**

**Dati NON migrati** (nessun equivalente in v18):

- `partner_document_number`, `partner_document_date`
- `taxes_ids`, `fiscal_position_id`
- Righe della dichiarazione (modello `declaration_line`)
- Limiti annuali (modello `yearly_limit`) — aggiustare manualmente la soglia delle
  singole dichiarazioni

**Risoluzione dei problemi:**

- *ValidationError sulle repartition lines durante l'installazione*: lo script di
  migrazione aggiunge automaticamente le repartition lines mancanti sulle imposte di
  gruppo per lo split payment. Se l'errore persiste, verificare che `openupgradelib`
  sia installato correttamente.

- *Errore di chiave duplicata su posizioni fiscali o imposte durante l'installazione
  di l10n_it_edi_doi*: può accadere se il vecchio modulo aveva già creato gli stessi
  dati di posizione fiscale. L'installazione di `l10n_it_edi_doi` può fallire o
  mostrare un avviso. Rimuovere manualmente le mappature di posizione fiscale duplicate
  e riprovare.

- *Importo DI sulla fattura a 0 o approssimativo*: nel percorso di migrazione normale,
  `l10n_it_edi_doi_amount` viene derivato dalla somma degli importi delle righe di
  dichiarazione v16 (valore esatto). Se la tabella delle righe era già assente al
  momento della migrazione, il fallback usa `ABS(amount_untaxed)` come approssimazione.
  Se si riscontrano importi a zero, aprire le fatture interessate e assegnare l'importo
  corretto nel tab "Dichiarazioni di Intento".

- *Limiti annuali non migrati*: il concetto non esiste in v18. Rivedere ogni
  dichiarazione e impostare il campo `threshold` con il valore appropriato.
