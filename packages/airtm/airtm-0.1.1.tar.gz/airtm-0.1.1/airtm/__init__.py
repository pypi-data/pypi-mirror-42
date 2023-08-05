from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution('AirTM').version
except DistributionNotFound:
    __version__ = '(local)'

from .airtm import *
