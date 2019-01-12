import json
import pytz
import pytest
from datetime import datetime

from adapters.cinema_city.enums import EventNameTagEndings

from adapters.cinema_city.theatres import CinemaCityTheatre
from adapters.enums import EventTags


class TestCinemaCityTagsParse:
    def test_no_tags(self, mocker):
        mocked_server_events_list = mocker.patch(
            "adapters.cinema_city.theatres.CinemaCityTheatre._get_event_list"
        )
        mocked_server_events_list.return_value = json.loads(
            json.dumps([{"Name": "Test Movie", "Dates": {"Date": "20/01/2019 10:10"}}])
        )
        adapter = CinemaCityTheatre(1, "test theatre", "test city", "test company")
        events_list = adapter.get_events(event_date=datetime.now(tz=pytz.utc))
        event = events_list[0]
        assert event.tags == []

    @pytest.mark.parametrize("tag_ending_enum", [e for e in EventNameTagEndings])
    def test_tagged(self, mocker, tag_ending_enum):
        mocked_server_events_list = mocker.patch(
            "adapters.cinema_city.theatres.CinemaCityTheatre._get_event_list"
        )
        mocked_server_events_list.return_value = json.loads(
            json.dumps(
                [
                    {
                        "Name": "Test Movie" + tag_ending_enum.value,
                        "Dates": {"Date": "20/01/2019 10:10"},
                    }
                ]
            )
        )
        adapter = CinemaCityTheatre(1, "test theatre", "test city", "test company")
        events_list = adapter.get_events(event_date=datetime.now(tz=pytz.utc))
        event = events_list[0]
        if "Hebrew" in tag_ending_enum.name:
            expected_event_tags = [EventTags.Hebrew]
        elif "English" in tag_ending_enum.name:
            expected_event_tags = [EventTags.English]
        elif "Dubbed" in tag_ending_enum.name:
            expected_event_tags = [EventTags.DubbedHebrew]
        else:
            raise AssertionError("Unknown expected tag from tag ending enum")

        assert event.tags == expected_event_tags
