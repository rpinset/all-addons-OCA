import datetime

from .hr_timesheet_sheet_test_cases import HrTimesheetTestCases


class TestHrTimesheetSheetCreate(HrTimesheetTestCases):
    """
    Tests for timesheet create method with timezone handling.
    Employee timezone is Europe/Brussels (UTC+1 in winter, UTC+2 in summer).
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set employee timezone to Europe/Brussels for timezone boundary tests
        cls.user_id.tz = "Europe/Brussels"

    def test_create_timezone_boundary_next_day(self):
        """Test attendance at UTC date boundary that's next day in Brussels"""
        # Attendance at Jan 14, 23:30 UTC = Jan 15, 00:30 Brussels (UTC+1)
        # So it's Jan 15 in employee's timezone
        attendance = self._create_attendance(
            employee=self.employee,
            checkIn=datetime.datetime(2019, 1, 14, 23, 30, 0),
            checkOut=datetime.datetime(2019, 1, 15, 2, 0, 0),
        )
        # Timesheet for Jan 15-20
        timesheet = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee.id,
                "date_start": datetime.date(2019, 1, 15),
                "date_end": datetime.date(2019, 1, 20),
            }
        )
        # Should be included (check_in is Jan 15 in Brussels)
        self.assertIn(
            attendance.id,
            timesheet.attendances_ids.ids,
            "Attendance should be included (Jan 14 23:30 UTC = Jan 15 in Brussels)",
        )

    def test_create_outside_date_range_not_linked(self):
        """
        Attendance whose check_in is Jan 14 Brussels must not
        be linked to a Jan 15-20 sheet
        """
        # Jan 13, 23:30 UTC = Jan 14, 00:30 Brussels (UTC+1) —
        # Jan 14 locally, before sheet start
        attendance = self._create_attendance(
            employee=self.employee,
            checkIn=datetime.datetime(2019, 1, 13, 23, 30, 0),
        )
        timesheet = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee.id,
                "date_start": datetime.date(2019, 1, 15),
                "date_end": datetime.date(2019, 1, 20),
            }
        )
        self.assertNotIn(
            attendance.id,
            timesheet.attendances_ids.ids,
            "Attendance on Jan 14 Brussels time must not be linked to a Jan 15 sheet",
        )

    def test_create_open_attendance_linked(self):
        """Open attendance crossing the UTC midnight boundary must be linked"""
        # Jan 14, 23:30 UTC = Jan 15, 00:30 Brussels (UTC+1) — Jan 15 locally, within sheet
        attendance = self._create_attendance(
            employee=self.employee,
            checkIn=datetime.datetime(2019, 1, 14, 23, 30, 0),
            checkOut=False,
        )
        timesheet = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee.id,
                "date_start": datetime.date(2019, 1, 15),
                "date_end": datetime.date(2019, 1, 20),
            }
        )
        self.assertIn(
            attendance.id,
            timesheet.attendances_ids.ids,
            "Open attendance at Jan 15 00:30 Brussels must be linked",
        )


class TestHrTimesheetSheetCreateNegativeTZ(HrTimesheetTestCases):
    """
    Tests for timesheet create method with a UTC-behind timezone.
    Employee timezone is America/New_York (UTC-5 in winter).
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_id.tz = "America/New_York"

    def test_create_end_of_day_boundary_positive(self):
        """End-of-day UTC boundary expands correctly for a UTC-behind timezone"""
        # Jan 20, 04:30 UTC = Jan 19, 23:30 New York (UTC-5) — still Jan 19 locally
        attendance = self._create_attendance(
            employee=self.employee,
            checkIn=datetime.datetime(2019, 1, 20, 4, 30, 0),
        )
        timesheet = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee.id,
                "date_start": datetime.date(2019, 1, 15),
                "date_end": datetime.date(2019, 1, 19),
            }
        )
        self.assertIn(
            attendance.id,
            timesheet.attendances_ids.ids,
            "Attendance at Jan 19 23:30 NY time must be linked to sheet ending Jan 19",
        )

    def test_create_end_of_day_boundary_negative(self):
        """Attendance starting Jan 20 in NY must not be linked to a sheet ending Jan 19"""
        # Jan 20, 05:30 UTC = Jan 20, 00:30 New York (UTC-5) — Jan 20 locally
        attendance = self._create_attendance(
            employee=self.employee,
            checkIn=datetime.datetime(2019, 1, 20, 5, 30, 0),
        )
        timesheet = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee.id,
                "date_start": datetime.date(2019, 1, 15),
                "date_end": datetime.date(2019, 1, 19),
            }
        )
        self.assertNotIn(
            attendance.id,
            timesheet.attendances_ids.ids,
            "Attendance at Jan 20 00:30 NY time must NOT be linked to sheet ending Jan 19",
        )
