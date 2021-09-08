import pathlib
import typing

import click
from loguru import logger

from sqlite2pg import S2PLogger
from sqlite2pg import CONFIG_SCHEMA


@click.group(name="config", invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Configure sqlite2pg."""
    click.secho(
        "The `config` subcommand has not been implemented yet.",
        fg="red", bold=True,
    )


@cli.command(name="regen")
@click.pass_obj
def regen_command(obj: object) -> None:
    # prints "magic string"
    click.secho(
        "The `config regen` subcommand has not been implemented yet.",
        fg="red", bold=True,
    )
