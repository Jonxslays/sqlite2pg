import typing

import click


@click.command(name="cli")
def cli() -> None:
    click.echo("CLIIIIIII from migrate")
