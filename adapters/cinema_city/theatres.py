from adapters.cinema_city.lib import CinemaCityTheatre
from adapters.enums import CityNames, CompanyNames


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
