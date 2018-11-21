import logging
import os
import shutil
import time
from datetime import datetime
from glob import glob
import requests

from imoh import config

logger = config.make_logger(__file__)
logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
logging.getLogger('matplotlib').setLevel(logging.WARNING)

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


def download_reports(years=None, weeks=_weeks, save_folder=None, force_download=False):
    '''Crawls through IMoH website and downloads all excel files in the given weeks and years'''
    if years is None:
        logger.warning('years not specified. Downloading all years since 2004')
        years = _years
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


def refresh_reports(year=None, week=None, weeks_back=15, save_folder=None):
    t = datetime.utcnow()
    # if year == 'current':
    year = year or t.year
    year_range = range(year, year + 1)
    this_week = week or t.isocalendar()[1]
    if this_week < weeks_back:
        download_reports(range(year - 1, year), range(week - weeks_back, 54), save_folder, force_download=True)
        week_range = range(1, this_week + 1)
    else:
        week_range = range(this_week - weeks_back, this_week + 1)
    download_reports(year_range, week_range, save_folder, force_download=True)


def _delete_folder_contents(folder):
    for root, dirs, files in os.walk(folder):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def delete_reports(save_folder=None, with_backup=True):
    save_folder = save_folder or os.path.join('.', 'data')
    backup_folder = os.path.join('.', 'data.backup')
    if with_backup:
        os.makedirs(backup_folder, exist_ok=True)
        for fn in glob(os.path.join(save_folder,'**')):
            os.rename(fn, fn.replace(save_folder,backup_folder))
    else:
        _delete_folder_contents(save_folder)