"""CLI module for vater."""
import datetime
from typing import Tuple

import click

from vater import Client

DATE_HELP_MESSAGE = "Date to search the data from"


@click.group()
@click.option(
    "--url", type=str, help="API base url", default="https://wl-api.mf.gov.pl"
)
@click.pass_context
def cli(ctx: click.Context, url: str) -> None:
    """Initialize a vater client object."""
    ctx.obj = Client(base_url=url)


@cli.command(name="search-account")
@click.argument("account", type=str)
@click.option(
    "-d", "--date", default=str(datetime.date.today()), help=DATE_HELP_MESSAGE
)
@click.pass_obj
def search_account(client: Client, account: str, date: str) -> None:
    """Search subjects with given account."""
    click.echo(client.search_account(account=account, raw=True, date=date))


@cli.command(name="search-accounts")
@click.argument("accounts", nargs=-1, type=str)
@click.option(
    "-d", "--date", default=str(datetime.date.today()), help=DATE_HELP_MESSAGE
)
@click.pass_obj
def search_accounts(client: Client, accounts: Tuple[str], date: str) -> None:
    """Search subjects with given accounts."""
    click.echo(client.search_accounts(accounts, date=date, raw=True))


@cli.command(name="search-nip")
@click.argument("nip", type=str)
@click.option(
    "-d", "--date", default=str(datetime.date.today()), help=DATE_HELP_MESSAGE
)
@click.pass_obj
def search_nip(client: Client, nip: str, date: str) -> None:
    """Search subjects with given nip."""
    click.echo(client.search_nip(nip=nip, raw=True, date=date))


@cli.command(name="search-nips")
@click.argument("nips", nargs=-1, type=str)
@click.option(
    "-d", "--date", default=str(datetime.date.today()), help=DATE_HELP_MESSAGE
)
@click.pass_obj
def search_nips(client: Client, nips: Tuple[str], date: str) -> None:
    """Search subjects with given nips."""
    click.echo(client.search_nips(nips=nips, raw=True, date=date))


@cli.command(name="search-regon")
@click.argument("regon", type=str)
@click.option(
    "-d", "--date", default=str(datetime.date.today()), help=DATE_HELP_MESSAGE
)
@click.pass_obj
def search_regon(client: Client, regon: str, date: str) -> None:
    """Search subjects with given regon."""
    click.echo(client.search_regon(regon=regon, raw=True, date=date))


@cli.command(name="search-regons")
@click.argument("regons", type=str)
@click.option(
    "-d", "--date", default=str(datetime.date.today()), help=DATE_HELP_MESSAGE
)
@click.pass_obj
def search_regons(client: Client, regons: Tuple[str], date: str) -> None:
    """Search subjects with given regons."""
    click.echo(client.search_regons(regons=regons, raw=True, date=date))


@cli.command(name="check-nip")
@click.argument("nip", type=str)
@click.argument("account", type=str)
@click.option(
    "-d", "--date", default=str(datetime.date.today()), help=DATE_HELP_MESSAGE
)
@click.pass_obj
def check_nip(client: Client, nip: str, account: str, date: str) -> None:
    """Check if given nip and account belongs to the same subject."""
    click.echo(client.check_nip(nip=nip, account=account, date=date, raw=True))


@cli.command(name="check-regon")
@click.argument("regon", type=str)
@click.argument("account", type=str)
@click.option(
    "-d", "--date", default=str(datetime.date.today()), help=DATE_HELP_MESSAGE
)
@click.pass_obj
def check_regon(client: Client, regon: str, account: str, date: str) -> None:
    """Check if given regon and account belongs to the same subject."""
    click.echo(client.check_regon(regon=regon, account=account, date=date, raw=True))


if __name__ == "__main__":
    cli()
