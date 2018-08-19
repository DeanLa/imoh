from datetime import datetime
import logging
import sys
prefix = datetime.now().strftime('./log/weeklies/%y%m%d_%H%M%S')

from .io import *
from .data import *
