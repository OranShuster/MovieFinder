import json
from datetime import datetime
import os

import pytest
import pytz

from adapters.yes_planet.enums import EventListKeys, EventAttributeSets
from adapters.yes_planet.theatres import YesPlanetTheatre


class TestYesPlanetTagParsing:
    @pytest.fixture()
    def load_example(self):
        file_dir_path = os.path.dirname(os.path.realpath(__file__))
        example_path = os.path.join(file_dir_path, "yes_planet_example.json")
        with open(example_path, encoding="utf-8") as example:
            response_example = json.loads(example.read(), encoding="utf-8")[0]
        return response_example

    @pytest.mark.usefixtures("load_example")
    def test_no_tags(self, mocker, load_example):
        mocked_server_events_list = mocker.patch(
            "adapters.yes_planet.theatres.YesPlanetTheatre._get_event_list"
        )

        # Remove event attributes
        load_example[EventListKeys.Events][0][EventListKeys.Attributes] = []
        mocked_server_events_list.return_value = load_example

        adapter = YesPlanetTheatre(1, "test theatre", "test city", "test company")
        events_list = adapter.get_events(event_date=datetime.now(tz=pytz.utc))
        event = events_list[0]
        assert event.tags == []

    @pytest.mark.usefixtures("load_example")
    @pytest.mark.parametrize("current_tag_enum", [e for e in EventAttributeSets])
    def test_single_tags(self, mocker, load_example, current_tag_enum):
        mocked_server_events_list = mocker.patch(
            "adapters.yes_planet.theatres.YesPlanetTheatre._get_event_list"
        )

        # Remove event attributes
        attribute_list = list(current_tag_enum.value[0])
        parsed_tag = current_tag_enum.value[1]
        load_example[EventListKeys.Events][0][EventListKeys.Attributes] = attribute_list
        mocked_server_events_list.return_value = load_example

        adapter = YesPlanetTheatre(1, "test theatre", "test city", "test company")
        events_list = adapter.get_events(event_date=datetime.now(tz=pytz.utc))
        event = events_list[0]
        assert event.tags == [parsed_tag]
