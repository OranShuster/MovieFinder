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
