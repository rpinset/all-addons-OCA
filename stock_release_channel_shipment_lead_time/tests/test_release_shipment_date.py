# Copyright 2023 Camptocamp
# Copyright 2025 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

import pytz
from freezegun import freeze_time

from odoo import fields

from odoo.addons.stock_release_channel.tests.common import ChannelReleaseCase

to_datetime = fields.Datetime.to_datetime


class TestChannelReleaseShipmentLeadTime(ChannelReleaseCase):
    def test_shipment_date(self):
        self.channel.warehouse_id.calendar_id = False
        self.channel.process_end_time = 12
        self.channel.process_end_date = "2023-09-11"
        self.channel.shipment_lead_time = 4
        self.assertEqual(
            "2023-09-15",
            fields.Date.to_string(self.channel.shipment_date),
        )

    def _test_shipment_date_with_calendar(self):
        # DST ends on 2025-10-26
        self.channel.warehouse_id = self.wh
        self.channel.warehouse_id.partner_id.tz = "Europe/Brussels"
        wh_tz = pytz.timezone(self.channel.warehouse_id.partner_id.tz)
        self.channel.warehouse_id.calendar_id = self.env.ref(
            "resource.resource_calendar_std"
        )
        self.channel.process_end_date = "2025-10-20 12:00:00"
        self.channel.shipment_lead_time = 1
        self.assertEqual(
            "2025-10-21",
            fields.Date.to_string(self.channel.shipment_date),
        )
        # Dates with DST
        local_dt = wh_tz.localize(datetime.datetime(2025, 10, 20, 0, 30))
        self.channel.process_end_date = self.channel._naive(local_dt)
        self.channel.shipment_lead_time = 1
        self.assertEqual(
            "2025-10-21",
            fields.Date.to_string(self.channel.shipment_date),
        )
        local_dt = wh_tz.localize(datetime.datetime(2025, 10, 20, 23, 30))
        self.channel.process_end_date = self.channel._naive(local_dt)
        self.channel.shipment_lead_time = 1
        self.assertEqual(
            "2025-10-21",
            fields.Date.to_string(self.channel.shipment_date),
        )
        local_dt = wh_tz.localize(datetime.datetime(2025, 10, 17, 0, 30))
        self.channel.process_end_date = self.channel._naive(local_dt)
        self.channel.shipment_lead_time = 1
        self.assertEqual(
            "2025-10-20",
            fields.Date.to_string(self.channel.shipment_date),
        )
        local_dt = wh_tz.localize(datetime.datetime(2025, 10, 17, 23, 30))
        self.channel.process_end_date = self.channel._naive(local_dt)
        self.channel.shipment_lead_time = 1
        self.assertEqual(
            "2025-10-20",
            fields.Date.to_string(self.channel.shipment_date),
        )
        # Dates over DST
        local_dt = wh_tz.localize(datetime.datetime(2025, 10, 24, 00, 30))
        self.channel.process_end_date = self.channel._naive(local_dt)
        self.channel.shipment_lead_time = 1
        self.assertEqual(
            "2025-10-27",
            fields.Date.to_string(self.channel.shipment_date),
        )
        local_dt = wh_tz.localize(datetime.datetime(2025, 10, 24, 23, 30))
        self.channel.process_end_date = self.channel._naive(local_dt)
        self.channel.shipment_lead_time = 1
        self.assertEqual(
            "2025-10-27",
            fields.Date.to_string(self.channel.shipment_date),
        )
        # Dates without DST
        local_dt = wh_tz.localize(datetime.datetime(2025, 10, 27, 0, 30))
        self.channel.process_end_date = self.channel._naive(local_dt)
        self.channel.shipment_lead_time = 1
        self.assertEqual(
            "2025-10-28",
            fields.Date.to_string(self.channel.shipment_date),
        )
        local_dt = wh_tz.localize(datetime.datetime(2025, 10, 27, 23, 30))
        self.channel.process_end_date = self.channel._naive(local_dt)
        self.channel.shipment_lead_time = 1
        self.assertEqual(
            "2025-10-28",
            fields.Date.to_string(self.channel.shipment_date),
        )
        local_dt = wh_tz.localize(datetime.datetime(2025, 10, 31, 0, 30))
        self.channel.process_end_date = self.channel._naive(local_dt)
        self.channel.shipment_lead_time = 1
        self.assertEqual(
            "2025-11-03",
            fields.Date.to_string(self.channel.shipment_date),
        )
        local_dt = wh_tz.localize(datetime.datetime(2025, 10, 31, 23, 30))
        self.channel.process_end_date = self.channel._naive(local_dt)
        self.channel.shipment_lead_time = 1
        self.assertEqual(
            "2025-11-03",
            fields.Date.to_string(self.channel.shipment_date),
        )

    @freeze_time("2025-10-20")
    def test_shipment_date_with_calendar_dst(self):
        """Test when we are in DST"""
        self._test_shipment_date_with_calendar()

    @freeze_time("2025-10-27")
    def test_shipment_date_with_calendar_nodst(self):
        """Test when we are without DST

        Dates should be the same. Current date shouldn't have an impact.
        """
        self._test_shipment_date_with_calendar()

    def test_delivery_date_shipment_lead_time(self):
        self.channel.warehouse_id = self.wh
        self.channel.warehouse_id.calendar_id = self.env.ref(
            "resource.resource_calendar_std"
        )
        self.channel.warehouse_id.partner_id.tz = "Europe/Brussels"
        self.channel.shipment_lead_time = 1
        dt = to_datetime("2025-01-02 08:00:00")  # Thursday
        gen = self.channel._next_delivery_date_shipment_lead_time(dt)
        result = next(gen)
        next_day = to_datetime("2025-01-02 23:00:00")  # Friday
        self.assertEqual(result, next_day)
        result = gen.send(dt)
        self.assertEqual(result, next_day)
        # around week-end
        dt = to_datetime("2025-01-03 08:00:00")  # Friday
        gen = self.channel._next_delivery_date_shipment_lead_time(dt)
        result = next(gen)
        next_day = to_datetime("2025-01-05 23:00:00")  # Monday
        self.assertEqual(result, next_day)
        result = gen.send(dt)
        self.assertEqual(result, next_day)
