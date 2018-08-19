import logging
import os
import time
from datetime import datetime
from glob import glob

import pandas as pd
import requests
import xlrd

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


def download_reports(years=_years, weeks=_weeks, force_download=False):
    '''Crawls through IMoH website and download all excel files in the given weeks and years'''
    # Create paths for logging files and download loaction
    base_loc = 'http://www.health.gov.il/PublicationsFiles/IWER'

    for year in years:
        logger.info(str(year))
        for week in weeks:
            # f = open(log_d, 'a')
            logger.info('{year}_{week}'.format(week=week, year=year))
            base_path = './data/weeklies/{year}_{week:02d}'.format(week=week, year=year)
            if file_exists(base_path) and not force_download:
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


def remove_bad_lines(df, week=0):
    ret = df.copy()
    removal = 'week no|{}|report|weekly|epidemiological|'.format(week)
    removal += 'for technical reasons|including cases updated|with or without other'
    idx = ret['Disease'].str.lower().str.contains(removal)
    return ret[~idx]


def process_file(file_path):
    stub = os.path.split(file_path)[-1]
    year, week = [int(x) for x in stub.split('.')[0].split('_')]
    try:
        df = pd.read_excel(file_path, sheet_name=str(week))
    except xlrd.biffh.XLRDError:
        logger.warning('{} is a bad file'.format(file_path))
        return pd.DataFrame()
    df = df.loc[df['Unnamed: 0'].notnull(), :].iloc[:, :-2]
    df['Unnamed: 0'] = df['Unnamed: 0'].astype(str)
    week_no = df.loc[df['Unnamed: 0'].str.lower().str.contains('week no'), :]
    names = week_no.iloc[1, :].astype(str)
    names[-2] = 'Total'
    names[-1] = 'CumTotal'
    df.columns = names
    df = df.rename(columns={'Week No.': 'Disease'})
    df = remove_bad_lines(df, week)
    df['year'] = year
    df['week'] = week
    return df


def clean_data(df):
    ordered = ['year', 'week', 'Disease', 'Afula', 'Akko', 'Ashqelon', 'Beer Sheva',
               'HaSharon', 'Hadera', 'Haifa', 'Jerusalem', 'Kinneret', 'Nazareth',
               'Petach Tiqwa', 'Ramla', 'Rehovot', 'Tel Aviv', 'Zefat', 'IDF', 'Total',
               'CumTotal']
    numeric = ordered[3:]
    ret = df[ordered].copy()
    for col in numeric:
        ret[col] = pd.to_numeric(ret[col], errors='coerce').fillna(0).astype(int)
    return ret

def make_data(backup=False):
    filenames = glob('./data/weeklies/20*_*.xls*')
    dfs = []
    for fn in filenames:
        dfs.append(process_file(fn))
        logger.debug(fn)
    data = pd.concat(dfs)
    data = data.rename(columns={"Ha'Sharon": "HaSharon"})
    if backup:
        try:
            data.to_pickle(backup)
        except:
            pass
    clean_data(data)
    return data
