from datetime import datetime

import click


@click.group(help='Everything that deals with downloading and wrangling files')
@click.pass_context
def cli(ctx):
    pass



current_year = datetime.now().year


@click.option('--force', 'force', is_flag=True, help='Force download even if file exists', show_default=True)
@click.option('--to', '-t', 'to_', default=current_year, show_default=True)
@click.option('--from', '-f', 'from_', default=2004, show_default=True)
@cli.command(help='Download all reports')
def download(from_, to_, force):
    from ..io import download_reports
    years = range(from_, to_ + 1)
    download_reports(years, force_download=force)


@click.option('--weeks-back', 'weeks_back', default=15, help='How many weeks back from current to refresh')
@cli.command(help='Refresh reports (Force Download)')
def refresh(weeks_back):
    from ..io import refresh_reports
    refresh_reports(weeks_back=weeks_back)
    click.echo('Done')


@click.option('--backup', 'backup', is_flag=False, show_default=True)
@cli.command(help='Delete all files in data folder')
def purge(backup):
    from ..io import delete_reports
    delete_reports(with_backup=backup)
    click.echo('Deleted')

@cli.command(help='Arrange data into machine readable format')
def arrange():
    from ..data import make_data
    make_data(backup=True)
    click.echo('Data Ready')

@cli.command(help='purge, refresh, make')
@click.pass_context
def create(ctx):
    ctx.invoke(purge, backup=False)
    ctx.invoke(refresh, weeks_back=15)
    ctx.invoke(arrange)
