import typing
from datetime import timedelta

import click
from loguru import logger

from sqlite2pg import DEV_LOG_CONFIG

__all__: typing.List[str] = [
    "S2PLogger",
]


LOG_FILE_FMT: str = "./sqlite2pg.{time:X}.log"


class S2PLogger:
    """Logging for the program."""

    FORMAT: str = "<green>{time}</green> | <level>{level: <8}</level> ||| <level>{message}</level>"

    @staticmethod
    def configure(
        enable: bool,
        to_cwd: bool,
        log_level: str,
        retention: int,
    ) -> None:
        """Configures  logger object."""

        logger.remove()

        if not enable:
            logger.disable("sqlite2pg")
            return

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
