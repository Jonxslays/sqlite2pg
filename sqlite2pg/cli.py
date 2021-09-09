import asyncio
import json
import pathlib
import typing

import click

from sqlite2pg import DEV_HOME_CONFIG, DEV_LOG_CONFIG
from sqlite2pg.modules import S2PLogger

__all__: typing.List[str] = [
    "CommandHandler",
    "CONFIG_SCHEMA",
]


COMMANDS_DIR: str = "./sqlite2pg/commands"
COMMANDS_FILES: typing.List[pathlib.Path] = [*pathlib.Path(".").glob(f"{COMMANDS_DIR}/*.py")]

ConfigSchemaT = typing.Mapping[str, typing.Mapping[str, typing.Union[str, bool, int]]]

CONFIG_SCHEMA: ConfigSchemaT = {
    "logging": {
        "enable": True,
        "level": "INFO",
        "to_cwd": False,
        "retention": 7,
    }
}


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

    @staticmethod
    def init_logging() -> None:
        try:
            with open(DEV_HOME_CONFIG / "config.json", "r") as f:
                data: typing.MutableMapping[str, typing.Any] = json.loads(f.read())

        except FileNotFoundError:
            config_path = DEV_HOME_CONFIG / "config.json"
            DEV_LOG_CONFIG.mkdir(parents=True, exist_ok=True)
            config_path.touch()

            schema = json.dumps(CONFIG_SCHEMA, indent=4, sort_keys=True)

            with open(config_path, "w") as f2:
                f2.write(schema)

        except PermissionError:
            click.echo(
                f"{click.style('unable to access config file.', fg='red', bold=True)}\n"
                "this is likely a permissions issue. please make sure the\n"
                "sqlite2pg config.json exists, and has the correct permissions.\nusing bash: "
                f"`{click.style('find / -wholename *sqlite2pg/config.json', fg='yellow', bold=True)}`"
            )
            click.secho("continuing anyways...", bold=True)

            S2PLogger.configure(enable=False, to_cwd=False, log_level="", retention=0)

        else:
            S2PLogger.configure(
                enable=data["logging"]["enable"],
                to_cwd=data["logging"]["to_cwd"],
                log_level=data["logging"]["level"],
                retention=data["logging"]["retention"],
            )


async def async_main() -> None:
    await asyncio.sleep(0)

    cli = CommandHandler(help="An SQLite3 to PostgreSQL database migration tool.")
    cli.init_logging()
    cli()


def main() -> None:
    asyncio.run(async_main())
