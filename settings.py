import inspect
import logging

from adapters.cinema_city import theatres as cc_theatres
from adapters.common import TheatreAdapter
from adapters.yes_planet import theatres as yp_theatres

DEBUG = True

AdapterBaseClass = TheatreAdapter
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
cc_adapters = []
for name, adapter in inspect.getmembers(cc_theatres, inspect.isclass):
    if adapter.__module__ == cc_theatres.__name__:
        if issubclass(adapter, AdapterBaseClass):
            cc_adapters.append(adapter())

yp_adapters = []
for name, adapter in inspect.getmembers(yp_theatres, inspect.isclass):
    if adapter.__module__ == yp_theatres.__name__:
        if issubclass(adapter, AdapterBaseClass):
            yp_adapters.append(adapter())

adapters = cc_adapters + yp_adapters
