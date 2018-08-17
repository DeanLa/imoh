import logging
import os
import time
from datetime import datetime

import requests

from imoh import config

prefix = datetime.now().strftime('./log/weeklies/%y%m%d_%H%M%S')
logger = logging.getLogger(__file__)
logger.addHandler(config.get_fh('{}.log'.format(prefix)))
logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)

_weeks = range(1, 54)
_years = range(2014, 2018)


def get_file_name_options(year, week):
    options = ['{week:02d}_{year}.xls'.format(week=week, year=year),
               '{week}_{year}.xls'.format(week=week, year=year),
               '{week:02d}_{year}.xlsx'.format(week=week, year=year),
               '{week}_{year}.xlsx'.format(week=week, year=year)]
    return options


def download_one(url):
    x = requests.get(url)
    return x


def save_excel(req, path):
    fn = open(path, 'wb')
    fn.write(req.content)
    logger.debug('{} SUCCESS'.format(req.url))


def file_exists(base_path, force_download=False):
    if force_download:
        return False
    return os.path.exists(base_path + '.xls') or os.path.exists(base_path + '.xlsx')


def download_reports(years=_years, weeks=_weeks):
    '''Crawls through IMoH website and download all excel files in the given weeks and years'''
    # Create paths for logging files and download loaction
    base_loc = 'http://www.health.gov.il/PublicationsFiles/IWER'

    for year in years:
        logger.info(str(year))
        for week in weeks:
            # f = open(log_d, 'a')
            logger.info('{year}_{week}'.format(week=week, year=year))
            base_path = './data/weeklies/{year}_{week:02d}'.format(week=week, year=year)
            if file_exists(base_path):
                logger.debug('Exists')
                continue
            # There are many different options of paths
            options = get_file_name_options(year, week)
            options = [base_loc + o for o in options]
            options += [o.replace('http', 'https') for o in options]
            for i, o in enumerate(options):
                time.sleep(0.1)
                filetype = o.split(".")[-1]
                url = o
                try:
                    path = '{path}.{ft}'.format(path=base_path, ft=filetype)
                    # Try different paths on remote, but always save on same path pattern locally
                    req = download_one(url, )
                    code = req.status_code
                    if code == 200:
                        not_foundnd = ['לא מצאנו', 'Sorry, something went wrong']
                        content = str(req.content)
                        # if any ([x in content for x in not_found]):
                        #     logger.debug('{} returned badly '.format(url))
                        # else:
                        save_excel(req, path)
                        break
                    elif code == 404:
                        logger.debug('{} not found'.format(url))
                    else:
                        logger.debug('{} returned with status code {}'.format(url, code))
                    if i == len(options) - 1:
                        logger.warning("{year}_{week:02d} FAILED\n".format(week=week, year=year))
                except Exception as e:
                    logger.exception(e)
