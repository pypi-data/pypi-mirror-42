name = 'buildabot'
__title__ = 'buildabot'
__author__ = 'Allen Lantz'
__copyright__ = 'Copyright 2019 Allen Lantz'
__version__ = '1.1.2'

from .bot import Bot
from .typer import Typer
from .logger import Logger
from . import utils
from .feature_manager import FeatureManager
from .feature import Feature
from .event_handler import EventHandler
from collections import namedtuple

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=1, minor=1, micro=2, releaselevel='beta', serial=0)
