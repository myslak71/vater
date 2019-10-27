"""CLI module for vater."""
import datetime
from typing import Tuple

import click

from vater import Client


@click.group()
@click.option(
    "--url", type=str, help="API base url", default="https://wl-api.mf.gov.pl"
)
@click.pass_context
def cli(ctx: click.Context, url: str) -> None:
    """Initialize a vater client object."""
    ctx.obj = Client(base_url=url)


@click.command(name="search-account")
@click.argument("account", type=str)
@click.option("-d", "--date", default=str(datetime.date.today()))
@click.pass_obj
def search_account(client: Client, account: str, date: str) -> None:
    """Search account."""
    click.echo(client.search_account(account=account, raw=True, date=date))


@click.command(name="search-accounts")
@click.argument("accounts", nargs=-1, type=str)
@click.option("-d", "--date", default=str(datetime.date.today()))
@click.pass_obj
def search_accounts(client: Client, accounts: Tuple[str], date: str) -> None:
    """Search accounts."""
    click.echo(client.search_accounts(accounts, date=date, raw=True))


@click.command(name="search-nip")
@click.argument("nip", type=str)
@click.option("-d", "--date", default=str(datetime.date.today()))
@click.pass_obj
def search_nip(client: Client, nip: str, date: str) -> None:
    """Search nip."""
    click.echo(client.search_nip(nip=nip, raw=True, date=date))


@click.command(name="search-nips")
@click.argument("nips", nargs=-1, type=str)
@click.option("-d", "--date", default=str(datetime.date.today()))
@click.pass_obj
def search_nips(client: Client, nips: Tuple[str], date: str) -> None:
    """Search nips."""
    click.echo(client.search_nips(nips=nips, raw=True, date=date))


@click.command(name="search-regon")
@click.argument("regon", type=str)
@click.option("-d", "--date", default=str(datetime.date.today()))
@click.pass_obj
def search_regon(client: Client, regon: str, date: str) -> None:
    """Search regon."""
    click.echo(client.search_regon(regon=regon, raw=True, date=date))


@click.command(name="search-regons")
@click.argument("regons", type=str)
@click.option("-d", "--date", default=str(datetime.date.today()))
@click.pass_obj
def search_regons(client: Client, regons: Tuple[str], date: str) -> None:
    """Search regons."""
    click.echo(client.search_regons(regons=regons, raw=True, date=date))


@click.command(name="check-nip")
@click.argument("nip", type=str)
@click.argument("account", type=str)
@click.option("-d", "--date", default=str(datetime.date.today()))
@click.pass_obj
def check_nip(client: Client, nip: str, account: str, date: str) -> None:
    """Check nip."""
    click.echo(client.check_nip(nip=nip, account=account, date=date, raw=True))


@click.command(name="check-regon")
@click.argument("regon", type=str)
@click.argument("account", type=str)
@click.option("-d", "--date", default=str(datetime.date.today()))
@click.pass_obj
def check_regon(client: Client, regon: str, account: str, date: str) -> None:
    """Check regon."""
    click.echo(client.check_regon(regon=regon, account=account, date=date, raw=True))


commands = (
    search_account,
    search_accounts,
    search_nip,
    search_nips,
    search_regon,
    search_regons,
    check_nip,
    check_regon,
)

for command in commands:
    cli.add_command(command)
