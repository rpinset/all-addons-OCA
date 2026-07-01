1. Open *Point of Sale > Configuration > a.sign RKSV* and create an
   `a.sign Certificate` record. For the *online* method, supply the
   certificate file together with the API user and password received from
   A-Trust.
2. Open *Point of Sale > Configuration > Point of Sale* and edit the POS you
   want to enable RKSV for. In the *Settings* tab, expand *RKSV Austria* and:
   - tick **RKSV Austria**;
   - select the *Method* (online or card);
   - enter the *Serial #* of the certificate created above;
   - enter the *Fiscal ID* (VAT number) of the company;
   - leave *POS ID* and *Encryption Key* empty to let the module generate
     defaults, or override them as needed.
3. Save the configuration and click **Assign** to lock the parameters and
   activate signing for new orders.

A scheduled action *POS a.sign: Sign Missed* runs daily and re-signs orders
that could not be signed at checkout time (for example because the online
service was temporarily unreachable).
