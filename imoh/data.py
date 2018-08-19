import os
from glob import glob

import pandas as pd
import xlrd

import logging
logger = logging.getLogger(__file__)


def _remove_bad_lines(df, week=0):
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
    names[-1] = 'SumTotal'
    df.columns = names
    df = df.rename(columns={'Week No.': 'Disease'})
    df = _remove_bad_lines(df, week)
    df['year'] = year
    df['week'] = week
    return df


def clean_data(df):
    ordered = ['year', 'week', 'Disease', 'Afula', 'Akko', 'Ashqelon', 'Beer Sheva',
               'HaSharon', 'Hadera', 'Haifa', 'Jerusalem', 'Kinneret', 'Nazareth',
               'Petach Tiqwa', 'Ramla', 'Rehovot', 'Tel Aviv', 'Zefat', 'IDF', 'Total',
               'SumTotal']
    numeric = ordered[3:]
    ret = df[ordered].copy()
    for col in numeric:
        ret[col] = pd.to_numeric(ret[col], errors='coerce').fillna(0).astype(int)
    ret = ret.rename(columns=lambda x: x.replace(' ', '_').replace("'", ""))
    return ret


def make_data(backup=False):
    filenames = glob('./data/weeklies/20*_*.xls*')
    dfs = []
    for fn in filenames:
        dfs.append(process_file(fn))
        logger.debug(fn)
    data = pd.concat(dfs)
    if backup:
        try:
            data.to_pickle(backup)
        except:
            logger.warning('cant create backup')
    data = clean_data(data)
    return data
