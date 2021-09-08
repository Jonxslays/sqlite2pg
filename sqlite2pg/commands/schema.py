import time
import typing
from pathlib import Path

import click
from loguru import logger

from sqlite2pg import Worker


FILE_HEADER = """/*
*
* DATABASE:
* '{}'
*
* File created by sqlite2pg at {:.0f} epoch.
* Use this generated file to import your schema at a later time.
* Thank you for using sqlite2pg.
*
*/\n"""


@click.command(name="schema")
@click.argument("database", type=click.Path(exists=True, path_type=Path))
@click.option("-f", "--file", type=Path, help="the optional filepath to write the schema to.")
@click.pass_context
def cli(ctx: click.Context, file: Path, database: Path) -> None:
    """Get table schema for an sqlite database."""

    worker: Worker = Worker()

    if file:
        if file.is_dir():
            logger.error("attempted to write schema to a directory. exiting...")
            click.secho("ERROR:", fg="red", bold=True)
            click.echo(f"can't write schema to '{file}'. it is a directory.")
            return

        elif file.exists():
            click.confirm(f"'{file}' exists. overwrite it?", default=False, abort=True)
            logger.debug("overwriting existing file in schema generation.")

        schema: typing.Mapping[str, typing.List[str]] = worker.get_sqlite_schema(database)

        with open(file, "w", encoding="utf-8") as f:
            f.write(FILE_HEADER.format(database, time.time()))

            for t, s in schema.items():
                f.write(f"\n-- Schema for table '{t}':\n{s[0]};\n")

    else:
        schema: typing.Mapping[str, typing.List[str]] = worker.get_sqlite_schema(database)

        for t, s in schema.items():
            click.secho(f"\nschema for table '{t}'", fg="green", bold=True)
            click.echo(f"{s[0]}")
