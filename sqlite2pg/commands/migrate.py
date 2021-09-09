import click


@click.command(name="migrate")
def migrate() -> None:
    """Make migrations from sqlite to postgres."""
    click.secho(
        "The `migrate` subcommand has not been implemented yet.",
        fg="red",
        bold=True,
    )
