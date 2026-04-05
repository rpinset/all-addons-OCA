**Italiano**

Consultare il file README di l10n_it_fatturapa.

É possibile esportare le fatture cliente con le righe articolo con un
CodiceTipo diverso dallo standard 'ODOO' creando un parametro
'fatturapa.codicetipo.odoo' (in Configurazione \> Funzioni tecniche \>
Parametri \> Parametri di sistema) con il codice voluto (tipicamente su
richiesta del cliente). Non è possibile impostare un diverso CodiceTipo
per cliente, al momento.

Per non mostrare nella fattura elettronica le righe descrittive (note, sezioni) presenti nella fattura, valorizzare il campo "Tipi di righe da nascondere".
Questo campo è presente in tre diversi posti, il valore impostato in uno di questi sovrascrive il valore presente nel successivo:
1. Nella fattura, scheda "Fatturazione elettronica", sezione "Configurazione";
2. Nel partner, scheda "Fatturazione elettronica";
3. In Contabilità > Configurazione > Impostazioni, sezione "Fatture elettroniche".

**English**

See l10n_it_fatturapa README file.

It is possible to export invoices with rows with a different CodiceTipo
from the default 'ODOO' by creating a parameter
'fatturapa.codicetipo.odoo' (in Settings \> Technical \> Parameters \>
System Parameters) with the desired code (tipically on customer's
request). It is not possible to set a different CodiceTipo by customer,
until now.

To hide the descriptive lines (notes, sections) present in the invoice from the electronic invoice, set the "Line Types to hide".
This field is present in three different places; the value set in one place overrides the value in the following place:
1. In the invoice, "Electronic Invoicing" tab, "Configuration" section;
2. In the partner, "Electronic Invoicing" tab;
3. In Accounting > Configuration > Settings, "Electronic Invoices" section.
