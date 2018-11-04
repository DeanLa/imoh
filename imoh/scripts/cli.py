import os
from datetime import datetime

import click


@click.group()
def cli():
    pass


@cli.group(help='')
def db():
    pass


@cli.group(help='Everything that deals with downloading and wrangling files')
def data():
    '''Everything that deals with downloading and wrangling files'''


@db.command()
def init():
    click.echo('Initialized the database')


current_year = datetime.now().year


@click.option('--from', '-f', 'from_', default=2004)
@click.option('--to', '-t', 'to_', default=current_year)
@click.option('--force', 'force', is_flag=True, help='Force download even if file exists')
@data.command(help='Download all reports')
def download(from_, to_, force):
    from ..io import download_reports
    years = range(from_, to_ + 1)
    download_reports(years, force_download=force)

@click.option('--weeks-back')
@data.command(help='Refresh reports')
def refresh():
    from ..io import refresh_reports
    refresh_reports()
