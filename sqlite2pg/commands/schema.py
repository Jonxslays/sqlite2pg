import typing

import click


@click.command(name="cli3")
def cli() -> None:
    click.echo("CLIIIIIII from schema")
