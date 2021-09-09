import click


@click.group(name="config", invoke_without_command=True)
@click.pass_context
def config(ctx: click.Context) -> None:
    """Configure sqlite2pg."""
    click.secho(
        "The `config` subcommand has not been implemented yet.",
        fg="red",
        bold=True,
    )


@config.command(name="regen")
@click.pass_obj
def regen_command(obj: object) -> None:
    # prints "magic string"
    click.secho(
        "The `config regen` subcommand has not been implemented yet.",
        fg="red",
        bold=True,
    )
