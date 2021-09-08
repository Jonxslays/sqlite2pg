import pathlib
import typing

import click
from loguru import logger

from sqlite2pg import S2PLogger


@click.group(name="config", invoke_without_command=True)
@click.option("-t", "--test", is_flag=True)
@click.pass_context
def cli(ctx: click.Context, test: bool) -> None:
    """sqlite2pg configuration options."""

    ctx.obj = "magic string"

    if ctx.invoked_subcommand is None:
        click.echo("there was no subcommand")

    if test:
        click.secho("IT WAS A TEST!!!", fg="green", bold=True)
    else:
        click.echo("CLIIIIIII from config")


@cli.command(name="regen")
@click.pass_obj
def regen_command(obj: object) -> None:
    # prints "magic string"
    click.echo(obj)
