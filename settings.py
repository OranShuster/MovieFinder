import logging

from adapters.cinema_city.theatres import CinemaCityRishonLeZion
from adapters.yes_planet.theatres import YesPlanetRishonLeZion

DEBUG = True

# Disable requests and urllib3 logging
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

stream_handler = logging.StreamHandler()
logging_format = "%(asctime)s [%(levelname)s] [%(name)s] [%(funcName)s] - %(message)s"

logging.basicConfig(
    handlers=[stream_handler],
    format=logging_format,
    level=logging.DEBUG if DEBUG else logging.INFO,
)

adapters = [CinemaCityRishonLeZion(), YesPlanetRishonLeZion()]
