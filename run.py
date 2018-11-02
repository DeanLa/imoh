import logging

from imoh import *

logger = logging.getLogger(__file__)

if __name__ == '__main__':
    # refresh_reports(weeks_back=25)
    # download_reports([2018],weeks=range(36,42))
    # process_file('./data/weeklies/2018_01.xlsx')
    data = make_data(backup='./data/backup.pickle')
    # data[['year', 'week', 'Disease', 'Afula', 'Akko', 'Ashqelon', 'Beer Sheva',
    #    'HaSharon', 'Hadera', 'Haifa', 'Jerusalem', 'Kinneret', 'Nazareth',
    #    'Petach Tiqwa', 'Ramla', 'Rehovot', 'Tel Aviv', 'Zefat', 'IDF', 'Total',
    #    'SumTotal']].to_pickle('./data/data.pickle')
    data.to_pickle('./181101.pickle')
