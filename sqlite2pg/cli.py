import logging
import time
import typing

import click

from sqlite2pg import LogConfig

__all__: typing.List[str] = [
    "CommandHandler",
]


log_lvls: typing.Mapping[str, int] = {
    "notset": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "error": logging.ERROR,
    "warn": logging.WARN,
    "warning": logging.WARNING,
    "critical": logging.CRITICAL,
    "fatal": logging.FATAL,
}


class CommandHandler:
    """Wrapper class for the command parser."""

    __slots__: typing.Sequence[str] = ("log")

    @click.command(name="main")
    @click.option(
        "--log-file",
        default=f"./slqlite2pg-{time.time():.0f}.log",
        help="Path to the log file you would like to use."
    )
    @click.option(
        "--log-lvl-file",
        default="info",
        help="The logging level to use for the log file."
    )
    @click.option(
        "--log-lvl-stream",
        default="info",
        help="The logging level to use for the stream handler."
    )
    @click.option(
        "--migrate",
        is_flag=True,
        help="Include a full data migration."
    )
    def main_cli(
        log_file: click.Option,
        log_lvl_file: click.Option,
        log_lvl_stream: click.Option,
        migrate: click.Option,
    ) -> logging.Logger:
        """An Sqlite3 to Postgresql database migration tool.
        By default sqlite2pg will only generate schema. Please add the
        --migration flag to migrate your data.
        """

        if log_lvl_file.lower() not in log_lvls.keys():
            raise click.BadOptionUsage("log lvl file")

        if log_lvl_stream.lower() not in log_lvls.keys:
            raise click.BadOptionUsage("log lvl stream")

        logger: logging.Logger = LogConfig.new(
            log_file,
            stream_level=log_lvls[log_lvl_stream],
            file_level=log_lvls[log_lvl_file],
        )

        if migrate:
            click.echo("were migrating")

        click.echo(log_file)
        click.echo(log_lvl_file)
        click.echo(log_lvl_stream)

        click.echo("done")

        return logger
