The backend model `mercadolibre.backend` is the component collection. Dispatch loads
every component with usage `notification.handler` on `mercadolibre.notification` and
keeps the one whose `_topic` equals the payload topic. A handler with an empty `_topic`
marks the notification skipped.

`_apply_on` has to be an Odoo model name. The Mercado Libre topic is not a model, so a
later addon selects its topic with `_topic`.

Register a handler for one topic in another addon:

    class OrderNotificationHandler(Component):
        _name = "mercadolibre.notification.handler.orders"
        _inherit = "mercadolibre.notification.handler"
        _apply_on = "mercadolibre.notification"
        _usage = "notification.handler"
        _topic = "orders_v2"

        def handle(self):
            notification = self.work.notification
            ...

The HTTP adapter usage is `backend.adapter`. Child adapters inherit
`mercadolibre.adapter` and set the resource path. Token refresh takes a row lock on the
backend because the refresh token is single-use.

Set `QUEUE_JOB__NO_DELAY=1` to run jobs inline while developing.
