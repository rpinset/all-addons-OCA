# Copyright 2026 TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, TransactionCase

# 1x1 transparent GIF, used as a dummy signature image. This is the canonical
# test image used across Odoo core: unlike a minimal PNG, its getexif() does not
# re-trigger an image load during ir.attachment post-processing, which some
# Pillow versions choke on ("Truncated File Read") for tiny PNGs.
SIGNATURE = b"R0lGODdhAQABAIAAAP///////ywAAAAAAQABAAACAkQBADs="


class TestFSMDigitizedSignature(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Order = self.env["fsm.order"]
        self.test_location = self.env.ref("fieldservice.test_location")

    def test_signature_fields(self):
        """The signature fields exist and persist on the order."""
        order = self.Order.create({"location_id": self.test_location.id})
        order.write(
            {
                "signature": SIGNATURE,
                "signed_by": "John Doe",
            }
        )
        self.assertEqual(order.signature, SIGNATURE)
        self.assertEqual(order.signed_by, "John Doe")

    def test_signed_on_autofill(self):
        """signed_on is stamped automatically when signing via the form."""
        with Form(self.Order, view="fieldservice.fsm_order_form") as form:
            form.location_id = self.test_location
            self.assertFalse(form.signed_on)
            form.signature = SIGNATURE
            self.assertTrue(form.signed_on)
        order = form.save()
        self.assertTrue(order.signed_on)

    def test_signature_not_copied(self):
        """Signature data is not carried over when duplicating an order."""
        order = self.Order.create(
            {
                "location_id": self.test_location.id,
                "signature": SIGNATURE,
                "signed_by": "John Doe",
            }
        )
        order.signed_on = order.write_date
        copy = order.copy()
        self.assertFalse(copy.signature)
        self.assertFalse(copy.signed_by)
        self.assertFalse(copy.signed_on)
