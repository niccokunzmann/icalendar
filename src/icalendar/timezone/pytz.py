"""Use pytz timezones."""
import pytz
from datetime import datetime


class PYTZ:
    """Provide icalendar with timezones from pytz."""

    def make_utc(self, value):
        """See icalendar.timezone.tzp.make_utc."""
        if getattr(value, 'tzinfo', False) and value.tzinfo is not None:
            return value.astimezone(pytz.utc)
        else:
            # assume UTC for naive datetime instances
            return pytz.utc.localize(value)

    def knows_timezone_id(self, id: str) -> bool:
        """Whether the timezone is already cached by the implementation."""
        return id in pytz.all_timezones

    def fix_pytz_rrule_until(self, rrule, component):
        """Make sure the until value works."""
        if not {'UNTIL', 'COUNT'}.intersection(component['RRULE'].keys()):
            # pytz.timezones don't know any transition dates after 2038
            # either
            rrule._until = datetime(2038, 12, 31, tzinfo=pytz.UTC)
