import logging
import sys
from datetime import datetime

FIRST_DAY_OF_YEAR = {
    2004:'2003-12-28',
    2005:'2005-01-02',
    2006:'2006-01-01',
    2007:'2007-12-31',
    2008:'2007-12-30',
    2009:'2009-01-04',
    2010:'2010-01-03',
    2011:'2011-01-02',
    2012:'2012-01-01',
    2013:'2012-12-30',
    2014:'2013-12-29',
    2015:'2015-01-04',
    2016:'2016-01-03',
    2017:'2017-01-01',
    2018:'2017-12-31',
}
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

