Install this module together with OCA `connector` 19.0. `connector` depends on
`component`, `component_event`, and `queue_job`.

The HTTP client uses the Python package `requests`.

Enable the job runner. In `odoo.conf`:

    [queue_job]
    channels = root:2,root.mercadolibre.import:2,root.mercadolibre.export:1,root.mercadolibre.webhook:2

Start Odoo with `--load=base,web,queue_job` and more than one worker.
