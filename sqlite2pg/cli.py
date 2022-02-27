import asyncio
import json
import pathlib
import typing

import click

__all__ = ["CommandHandler"]

COMMANDS_DIR: str = "./sqlite2pg/commands"
COMMANDS_FILES: typing.List[pathlib.Path] = [*pathlib.Path(".").glob(f"{COMMANDS_DIR}/*.py")]


class CommandHandler(click.MultiCommand):
    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(*args, **kwargs)

    def list_commands(self, ctx: click.Context) -> typing.List[str]:
        commands: typing.List[str] = []
        commands.extend(p.stem for p in COMMANDS_FILES)
        commands.sort()

        return commands

    def get_command(self, ctx: click.Context, name: str) -> typing.Optional[click.Command]:
        namespace: typing.Dict[str, object] = {}
        filepath = pathlib.Path(f"{COMMANDS_DIR}/{name}.py")

        with open(filepath, "r") as f:
            code = compile(f.read(), filepath, "exec")
            eval(code, namespace, namespace)

        cmd = namespace.get(name)

        return cmd if isinstance(cmd, click.Command) else None


async def async_main() -> None:
    cli = CommandHandler(help="An SQLite3 to PostgreSQL database migration tool.")
    cli()


def main() -> None:
    asyncio.run(async_main())
