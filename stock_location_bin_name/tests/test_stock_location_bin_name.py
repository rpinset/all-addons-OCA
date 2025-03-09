from odoo.exceptions import ValidationError
from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestStockLocationBinName(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.location_obj = cls.env["stock.location"]
        # Create the following structure:
        # # [Zone Location]
        # # # [Area Location]
        # # # # [Bin Location]
        cls.location_zone = cls.location_obj.create(
            {
                "name": "Zone Location",
                "is_zone": True,
            }
        )
        cls.location_area = cls.location_obj.create(
            {"name": "Area Location", "location_id": cls.location_zone.id}
        )

        cls.location_bin = cls.location_obj.create(
            {
                "name": "Bin Location",
                "zone_location_id": cls.location_zone.id,
                "area_location_id": cls.location_area.id,
                "location_id": cls.location_area.id,
                "location_kind": "bin",
                "usage": "internal",
            }
        )

    def test_location_name_format(self):
        """Test location name with format string from area"""

        with Form(self.location_area) as location_form:
            location_form.location_name_format = (
                "{area}-{corridor}-{posx:0>3}.{rack:0>3}.{level:0>2}"
            )

        with Form(self.location_bin) as location_form:
            location_form.corridor = "A"
            location_form.rack = "51"
            location_form.posx = 123
            location_form.level = "42"

        self.assertEqual(self.location_bin.name, "Area Location-A-123.051.42")

    def test_location_name_format_in_zone(self):
        """Test location name with format string from zone"""

        with Form(self.location_zone) as location_form:
            location_form.location_name_format = (
                "{area}-{corridor}-{level:0>2}-{posx}{posy}{posz}.{rack:0>3}"
            )

        with Form(self.location_bin) as location_form:
            location_form.corridor = "Z"
            location_form.rack = "5"
            location_form.posx = 1
            location_form.posy = 2
            location_form.posz = 3
            location_form.level = "2"

        self.assertEqual(self.location_bin.name, "Zone Location-Z-02-123.005")

    def test_location_bin_with_name_format(self):
        """Test location constraint with location name format in a bin location"""

        regex = "Location Name Format cannot be set on 'bin' type locations."
        with self.assertRaisesRegex(ValidationError, regex):
            self.location_obj.create(
                {
                    "name": "Local",
                    "location_id": self.location_area.id,
                    "location_name_format": "{area}-{corridor}{level:0>2}",
                    "usage": "internal",
                    "location_kind": "bin",
                    "zone_location_id": self.location_zone.id,
                    "area_location_id": self.location_area.id,
                }
            )

    def test_onchange_non_bin_location(self):
        """Test onchange does nothing for non-bin locations"""
        test_location = self.location_obj.create(
            {
                "name": "Test Location",
                "location_id": self.location_area.id,
                "usage": "internal",
                "location_kind": "area",
            }
        )
        original_name = test_location.name

        with Form(test_location) as location_form:
            location_form.corridor = "A"
            location_form.level = "1"

        self.assertEqual(test_location.name, original_name)

    def test_onchange_no_area_format(self):
        """Test onchange when area has no location_name_format"""
        self.location_area.location_name_format = False

        test_bin = self.location_obj.create(
            {
                "name": "Test Bin",
                "location_id": self.location_area.id,
                "usage": "internal",
                "location_kind": "bin",
            }
        )
        original_name = test_bin.name

        with Form(test_bin) as bin_form:
            bin_form.corridor = "B"
            bin_form.level = "2"

        self.assertEqual(test_bin.name, original_name)

    def test_onchange_no_parent_area(self):
        """Test onchange when there is no parent area with format"""
        orphan_bin = self.location_obj.create(
            {"name": "Orphan Bin", "usage": "internal", "location_kind": "bin"}
        )
        original_name = orphan_bin.name

        with Form(orphan_bin) as bin_form:
            bin_form.corridor = "C"
            bin_form.level = "3"

        self.assertEqual(orphan_bin.name, original_name)
