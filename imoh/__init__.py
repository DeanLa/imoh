import os
from urllib import URLopener
from datetime import datetime
import pandas as pd


class Disease(pd.DataFrame):
    def __init__(self, name, *args, **kwargs):
        pd.DataFrame.__init__(self, *args, **kwargs)
        assert type(name) == str, "Disease is a string"
        self.name = name.lower()

    def find_disease(self, data_folder='./data/weeklies'):
        pass


_weeks = range(1, 54)
_years = range(2000, 2016)


def download_reports(years=_years, weeks=_weeks):
    '''Crawls through IMoH website and download all excel files in the given weeks and years'''
    # Create paths for logging files and download loaction
    prefix = datetime.now().strftime('./log/weeklies/%y%m%d_%H%M%S_')
    log_d = prefix + "downloads.log"
    log_f = prefix + "FAILED.log"
    base_loc = 'http://www.health.gov.il/PublicationsFiles/IWER'
    # URL object
    my_file = URLopener()

    for year in years:
        print "\n", year,
        for week in weeks:
            f = open(log_d, 'a')
            f.write('\n{year}_{week}: '.format(week=week, year=year))
            # There are many different options of paths
            options = ['{base}{week:02d}_{year}.xls'.format(base=base_loc, week=week, year=year),
                       '{base}{week}_{year}.xls'.format(base=base_loc, week=week, year=year),
                       '{base}{week:02d}_{year}.xlsx'.format(base=base_loc, week=week, year=year),
                       '{base}{week}_{year}.xlsx'.format(base=base_loc, week=week, year=year)]
            for i, o in enumerate(options):
                filetype = o.split(".")[-1]
                try:
                    # Try different paths on remote, but always save on same path locally
                    my_file.retrieve(o,
                                     './data/weeklies/{year}_{week:02d}.{ft}'.format(week=week, year=year, ft=filetype))
                    # If succeeds write which filetype (xls/x) was saved
                    f.write('{ft}'.format(ft=filetype), )
                    # If downloads succeeds move close the log file and break the loop
                    f.close()
                    break
                except:
                    # When option excepted, write try number to the log
                    f.write("{} ".format(i + 1))
                    # If all options were exhausted, it has failed.
                    if i == len(options) - 1 and week != 53:
                        print "== {year}_{week:02d} FAILED ==".format(week=week, year=year),
                        with open(log_f, 'a') as failed:
                            failed.write("{year}_{week:02d} FAILED\n".format(week=week, year=year))
                        f.write("FAILED")
                        f.close()
        f.close()
