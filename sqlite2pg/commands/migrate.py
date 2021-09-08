import typing

import click


@click.command(name="cli")
def cli() -> None:
    """Make migrations from sqlite to postgres."""
    click.secho(
        "The `migrate` subcommand has not been implemented yet.",
        fg="red", bold=True,
    )
