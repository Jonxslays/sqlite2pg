import time
from pathlib import Path

import click
from loguru import logger

from sqlite2pg import CleanSchemaT, Worker

FILE_HEADER = """/*
*
* DATABASE:
* '{}'
*
* This schema is in '{}' format.
*
* File created by sqlite2pg at {:.0f} epoch.
* Use this generated file to import your schema at a later time.
* Thank you for using sqlite2pg.
*
*/\n"""


@click.command(name="schema")
@click.argument("database", type=click.Path(exists=True, path_type=Path))
@click.option("-f", "--file", type=Path, help="The optional PATH to write the schema to.")
@click.option(
    "-c",
    "--convert",
    is_flag=True,
    default=False,
    help="If added, this flag converts the schema to postgres syntax.",
)
@click.pass_context
def schema(ctx: click.Context, database: Path, file: Path, convert: bool) -> None:
    """Get table schema from an sqlite DATABASE.
    By default sqlite2pg will write the schema to stdout.

    DATABASE The database to get the schema from.
    """

    worker: Worker = Worker()
    schema: CleanSchemaT = worker.get_sqlite_schema(database)

    if convert:
        schema = worker.convert_sqlite_to_pg(schema)

    if file:
        if file.is_dir():
            logger.error("attempted to write schema to a directory. exiting...")
            click.secho("ERROR:", fg="red", bold=True)
            click.echo(f"can't write schema to '{file}'. it is a directory.")
            return

        elif file.exists():
            click.confirm(f"'{file}' exists. overwrite it?", default=False, abort=True)
            logger.debug("overwriting existing file in schema generation.")

        with open(file, "w", encoding="utf-8") as f:
            f.write(
                FILE_HEADER.format(database, "PostgreSQL" if convert else "SQLite", time.time()),
            )

            for t, s in schema.items():
                f.write(f"\n-- Schema for table '{t}':\n{s[0]}\n")

    else:
        for t, s in schema.items():
            click.secho(f"\n-- schema for table '{t}'", fg="green", bold=True)
            click.echo(f"{s[0]}")
