import logging
from datetime import datetime
from typing import List, Tuple

import requests
from babel.dates import format_datetime

from adapters.cinema_city import enums
from adapters.common import Event, TheatreAdapter
from adapters.enums import CityNames, CompanyNames, EventTags

logger = logging.getLogger("CinemaCityTheatre")


# noinspection PyRedundantParentheses
class CinemaCityTheatre(TheatreAdapter):
    def _parse_event_tags(self, event_name: str) -> Tuple[str, List[EventTags]]:
        # First check for hyphen versions
        query_ind = event_name.find(enums.EventNameTagEndings.EnglishWithHyphen.value)
        if query_ind != -1:
            return (event_name[:query_ind], [EventTags.English])

        query_ind = event_name.find(enums.EventNameTagEndings.HebrewWithHyphen.value)
        if query_ind != -1:
            return (event_name[:query_ind], [EventTags.Hebrew])

        query_ind = event_name.find(enums.EventNameTagEndings.DubbedWithHyphen.value)
        if query_ind != -1:
            return (event_name[:query_ind], [EventTags.DubbedHebrew])

        query_ind = event_name.find(enums.EventNameTagEndings.English.value)
        if query_ind != -1:
            return event_name[:query_ind], [EventTags.English]

        query_ind = event_name.find(enums.EventNameTagEndings.Hebrew.value)
        if query_ind != -1:
            return (event_name[:query_ind], [EventTags.Hebrew])

        query_ind = event_name.find(enums.EventNameTagEndings.Dubbed.value)
        if query_ind != -1:
            return (event_name[:query_ind], [EventTags.DubbedHebrew])

        return event_name, []

    def _get_event_list(self, event_date: datetime):
        today_babel = format_datetime(
            event_date, format=enums.DATE_URL_FORMAT, locale=enums.THEATRE_LOCALE
        )
        url = enums.EVENT_LIST_URL.format(theatre_id=self.theatre_id, date=today_babel)
        logger.debug("Get event list from server using url - {}".format(url))
        response = requests.get(url)
        return response.json()

    def _parse_event_list(self, event_list_from_server: list):
        parsed_event_list = []
        for event in event_list_from_server:
            event_name = event[enums.EventListKeys.Name.value]
            event_datetime = datetime.strptime(
                event[enums.EventListKeys.Dates.value][enums.EventListKeys.Date.value],
                enums.EVENT_LIST_DATETIME_FORMAT,
            )
            event_name, tags = self._parse_event_tags(event_name=event_name)

            new_event = Event(
                name=event_name,
                date=event_datetime,
                city=self.city,
                company=self.company,
                tags=tags,
            )
            parsed_event_list.append(new_event)

        return parsed_event_list

    def get_events(self, event_date):
        self.validate_event_date(event_date=event_date)
        event_list_from_server = self._get_event_list(event_date)
        parsed_event_list = self._parse_event_list(event_list_from_server)
        return parsed_event_list


class CinemaCityRishonLeZion(CinemaCityTheatre):
    THEATRE_ID = 1173

    def __init__(self):
        super(CinemaCityRishonLeZion, self).__init__(
            display_name="Cinema City Rishon LeZion",
            theatre_id=self.THEATRE_ID,
            company=CompanyNames.CinemaCity,
            city=CityNames.RishonLeZion,
        )


class CinemaCityGlilot(CinemaCityTheatre):
    THEATRE_ID = 1170

    def __init__(self):
        super(CinemaCityGlilot, self).__init__(
            display_name="Cinema City Glilot",
            theatre_id=self.THEATRE_ID,
            company=CompanyNames.CinemaCity,
            city=CityNames.Glilot,
        )
