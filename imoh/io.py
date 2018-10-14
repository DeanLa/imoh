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
_years = range(2004, 2019)


def _get_file_name_options(year, week):
    base_path = 'http://www.health.gov.il/PublicationsFiles/IWER'
    options = ['{base}{week:02d}_{year}.xls'.format(base=base_path, week=week, year=year),
               '{base}{week}_{year}.xls'.format(base=base_path, week=week, year=year),
               '{base}{week:02d}_{year}.xlsx'.format(base=base_path, week=week, year=year),
               '{base}{week}_{year}.xlsx'.format(base=base_path, week=week, year=year)]

    options_s = [o.replace('http', 'https') for o in options]
    return options + options_s


def _get_fileype_from_url(url):
    filetype = url.split(".")[-1]
    return filetype


def _download_file(url, path):
    req = requests.get(url)
    filetype = _get_fileype_from_url(url)
    path = '{path}.{ft}'.format(path=path, ft=filetype)
    # Try different paths on remote, but always save on same path pattern locally
    code = req.status_code
    if code == 200:
        _save_excel(req, path)
        return True
    elif code == 404:
        logger.debug('{} not found'.format(url))
        return False
    else:
        logger.debug('{} returned with status code {}'.format(url, code))
        return False

    return req


def _save_excel(req, path):
    fn = open(path, 'wb')
    fn.write(req.content)
    logger.debug('{} SUCCESS'.format(req.url))


def _file_exists(base_path):
    return os.path.exists(base_path + '.xls') or os.path.exists(base_path + '.xlsx')


def download_single_report(path, week, year):
    options = _get_file_name_options(year, week)
    for i, url in enumerate(options):
        time.sleep(0.1)
        try:
            if _download_file(url, path):
                return
            if i == len(options) - 1:
                logger.warning("{year}_{week:02d} FAILED\n".format(week=week, year=year))
        except Exception as e:
            logger.exception(e)


def download_reports(years=_years, weeks=_weeks, save_folder=None, force_download=False):
    '''Crawls through IMoH website and downloads all excel files in the given weeks and years'''
    save_folder = save_folder or os.path.join('.', 'data', 'weeklies')
    os.makedirs(save_folder, exist_ok=True)
    for year in years:
        for week in weeks:
            year_week = '{year}_{week:02d}'.format(week=week, year=year)
            logger.info(year_week)
            path = os.path.join(save_folder, year_week)
            if _file_exists(path) and not force_download:
                logger.info('Exists')
                continue
            download_single_report(path, week, year)


