from enum import Enum

from adapters.enums import EventTags

DATE_URL_FORMAT = "%Y-%m-%d"
EVENT_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
EVENT_LIST_URL = "https://www.yesplanet.co.il/en/data-api-service/v1/quickbook/10100/film-events/in-cinema/{theatre_id}/at-date/{date}"  # noqa


class EventListKeys(object):
    Name = "name"
    Body = "body"
    Films = "films"
    Events = "events"
    FilmId = "filmId"
    Id = "id"
    EventDateTime = "eventDateTime"
    Attributes = "attributeIds"


class EventAttributeSets(Enum):
    EnglishLanguage = ({"original-lang-en-us"}, EventTags.English)
    HebrewLanguage = ({"original-lang-he"}, EventTags.Hebrew)
    SubbedHebrew = ({"subbed", "first-subbed-lang-he"}, EventTags.SubbedHebrew)
    ScreenX2D = ({"screenx", "2d"}, EventTags.ScreenX2D)
    Event3D = ({"3d"}, EventTags.In3D)
