import logging
import sys
from datetime import datetime

prefix = datetime.now().strftime('./log/weeklies/%y%m%d_%H%M%S')
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# create file handler which logs even debug messages
def get_fh(filename):
    fh = logging.FileHandler(filename)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    return fh