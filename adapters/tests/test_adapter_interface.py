import pytest

import settings

from adapters.common import TheatreAdapter, today, Event


def verify_adapter_response(adapter_response):
    assert len(adapter_response) > 0
    for event in adapter_response:
        assert isinstance(event, Event)


class TestAdaptersParsedEventsType:
    @pytest.mark.parametrize("adapter_instance", settings.adapters)
    def test_adapter_today(self, adapter_instance: TheatreAdapter):
        adapter_response = adapter_instance.get_events(event_date=today())
        verify_adapter_response(adapter_response)
