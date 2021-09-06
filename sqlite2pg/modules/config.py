import logging
import time
import typing


__all__: typing.List[str] = [
    "Logger",
]


DEFAULT_LOG_FILE: str = f"./slqlite2pg-{time.time():.0f}.log"


class Logger(logging.Logger):
    """Logging for the program."""

    __slots__: typing.Sequence[str] = ()

    @staticmethod
    def new(
        stream_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        file_path: str = None,
    ) -> logging.Logger:
        """Initializes a new logger object and returns it.

        Args:
            stream_level: int
                The logging level to set for the stream handler. This will
                be the output to the terminal. Defaults to INFO.

            file_level: int
                The logging level to set for the stream handler. This will
                be the output to the terminal. Defaults to DEBUG.

            file_path: str
                The absolute or relative path you would like the log file
                to generated at. Defaults to './sqlite2pg-{%epoch%}.log'
                where {%epoch%} is the current epoch time.

        Returns:
            logging.Logger: The configured logger.
        """

        # Instantiate logger.
        _log: logging.Logger = logging.getLogger()
        _log.setLevel(logging.DEBUG)

        # Instantiate formatter.
        _logF: logging.Formatter = logging.Formatter(
            f"[%(asctime)s] %(levelname)8s ||| %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Instantiate streamhandler (stdout) and set log level.
        _logSh: logging.StreamHandler = logging.StreamHandler()
        _logSh.setLevel(stream_level)

        # Instantiate file handler.
        _logFh: logging.FileHandler = logging.FileHandler(
            file_path if file_path else DEFAULT_LOG_FILE
        )

        # Set file handler formatter, and log level.
        _logFh.setFormatter(_logF)
        _logFh.setLevel(file_level)

        # Add both handlers and return the Logger object.
        _log.addHandler(_logFh)
        _log.addHandler(_logSh)

        return _log
