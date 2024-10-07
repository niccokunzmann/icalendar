"""Test the VALARM compatibility of RFC 9074.

See https://www.rfc-editor.org/rfc/rfc9074.html
and also https://github.com/collective/icalendar/issues/657
"""
import pytest
from icalendar.prop import vText, vDDDTypes


@pytest.mark.parametrize(
    ("prop", "cls", "file", "alarm_index"),
    [
        ("UID", vText, "rfc_9074_example_1", 0),
        ("RELATED-TO", vText, "rfc_9074_example_2", 1),
        ("ACKNOWLEDGED", vDDDTypes, "rfc_9074_example_3", 0),
        ("PROXIMITY", vText, "rfc_9074_example_proximity", 0),
    ]
)
def test_calendar_types(events, prop, cls, file, alarm_index):
    """Check the types of the properties."""
    event = events[file]
    alarm = event.subcomponents[alarm_index]
    value = alarm[prop]
    assert isinstance(value, cls)
