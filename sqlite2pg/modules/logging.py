import logging
import typing
from datetime import timedelta
from pathlib import Path

import click
from loguru import logger

from sqlite2pg import DEV_HOME_CONFIG, DEV_LOG_CONFIG

__all__: typing.List[str] = [
    "S2PLogger",
]


LOG_FILE_FMT: str = "./slqlite2pg_{time}.log"


LOG_LEVELS: typing.Mapping[str, int] = {
    "TRACE": 5,
    "DEBUG": 10,
    "INFO": 20,
    "SUCCESS": 25,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}


class S2PLogger:
    """Logging for the program."""

    FORMAT: str = (
        "<green>{time}</green> | <level>{level: <8}</level> ||| <level>{message}</level>"
    )

    @staticmethod
    def configure(
        enable: bool,
        to_cwd: bool,
        log_level: str,
        retention: int,
    ) -> None:
        """Configures  logger object."""

        if not enable:
            logger.disable("sqlite2pg")
            return

        logger.remove()

        try:
            logger.add(
                LOG_FILE_FMT if to_cwd else (DEV_LOG_CONFIG / LOG_FILE_FMT),
                format=S2PLogger.FORMAT,
                level=log_level.upper(),
                retention=timedelta(days=retention),
            )

        except Exception as e:
            print(e)
            click.secho("ERROR:", fg="red", bold=True)
            click.echo(
                "invalid logging level retrieved from config.\n"
                "please validate your config or run `sqlite2pg config regen`."
            )
            exit(1)

        else:
            logger.debug("logging configuration completed.")
