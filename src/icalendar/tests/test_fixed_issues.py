import unittest

import datetime
import icalendar
import os
import pytz
import pytest
from dateutil import tz

try:
    import zoneinfo
except ModuleNotFoundError:
    from backports import zoneinfo

class TestIssues(unittest.TestCase):

    def test_issue_82(self):
        """Issue #82 - vBinary __repr__ called rather than to_ical from
                       container types
        https://github.com/collective/icalendar/issues/82
        """

        b = icalendar.vBinary('text')
        b.params['FMTTYPE'] = 'text/plain'
        self.assertEqual(b.to_ical(), b'dGV4dA==')
        e = icalendar.Event()
        e.add('ATTACH', b)
        self.assertEqual(
            e.to_ical(),
            b"BEGIN:VEVENT\r\nATTACH;ENCODING=BASE64;FMTTYPE=text/plain;"
            b"VALUE=BINARY:dGV4dA==\r\nEND:VEVENT\r\n"
        )

    def test_issue_116(self):
        """Issue #116/#117 - How to add 'X-APPLE-STRUCTURED-LOCATION'
        https://github.com/collective/icalendar/issues/116
        https://github.com/collective/icalendar/issues/117
        """
        event = icalendar.Event()
        event.add(
            "X-APPLE-STRUCTURED-LOCATION",
            "geo:-33.868900,151.207000",
            parameters={
                "VALUE": "URI",
                "X-ADDRESS": "367 George Street Sydney CBD NSW 2000",
                "X-APPLE-RADIUS": "72",
                "X-TITLE": "367 George Street"
            }
        )
        self.assertEqual(
            event.to_ical(),
            b'BEGIN:VEVENT\r\nX-APPLE-STRUCTURED-LOCATION;VALUE=URI;'
            b'X-ADDRESS="367 George Street Sydney \r\n CBD NSW 2000";'
            b'X-APPLE-RADIUS=72;X-TITLE="367 George Street":'
            b'geo:-33.868900\r\n \\,151.207000\r\nEND:VEVENT\r\n'
        )

        # roundtrip
        self.assertEqual(
            event.to_ical(),
            icalendar.Event.from_ical(event.to_ical()).to_ical()
        )
