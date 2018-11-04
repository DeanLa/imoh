import logging
import sys
from datetime import datetime
import os

FIRST_DAY_OF_YEAR = {
    2004: '2003-12-28',
    2005: '2005-01-02',
    2006: '2006-01-01',
    2007: '2007-12-31',
    2008: '2007-12-30',
    2009: '2009-01-04',
    2010: '2010-01-03',
    2011: '2011-01-02',
    2012: '2012-01-01',
    2013: '2012-12-30',
    2014: '2013-12-29',
    2015: '2015-01-04',
    2016: '2016-01-03',
    2017: '2017-01-01',
    2018: '2017-12-31',
}

# create formatter and add it to the handlers

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def make_logger(name, allow_new_dir=True):
    logs_dir = os.path.join('.', 'log', 'weeklies')
    prefix = os.path.join(logs_dir, datetime.now().strftime('%y%m%d_%H%M%S'))
    logger = logging.getLogger(name)
    if not os.path.exists(logs_dir):
        if allow_new_dir:
            os.makedirs(logs_dir, exist_ok=True)
        else:
            raise IOError()
    # prefix = datetime.now().strftime(os.path.join(logs_dir,'%y%m%d_%H%M%S'))

    logger.addHandler(_get_filehandler('{}.log'.format(prefix)))
    return logger


# create file handler which logs even debug messages
def _get_filehandler(filename):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(filename)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    return fh
