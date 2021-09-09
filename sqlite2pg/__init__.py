"""An SQLite3 to PostgreSQL database migration tool."""
import os
import typing
from pathlib import Path

if os.name == "nt":
    HOME_CONFIG = Path.home() / ".sqlite2pg"
    LOG_CONFIG = HOME_CONFIG / "logs"
else:
    HOME_CONFIG = Path.home() / ".config/sqlite2pg"
    LOG_CONFIG = HOME_CONFIG / "logs"

DEV_HOME_CONFIG = Path(".") / ".config/sqlite2pg"
DEV_LOG_CONFIG = DEV_HOME_CONFIG / "logs"

from .cli import *
from .modules import *

__version__: str = "0.1.4"
__author__: str = "Jonxslays"
__maintainer__: str = "Jonxslays"
__license__: str = "BSD-3-Clause"
__url__: str = "https://github.com/Jonxslays/sqlite2pg"

__all__: typing.List[str] = [
    "Worker",
    "S2PLogger",
    "Sqlite2pgError",
    "SqliteError",
    "LoggingConfigError",
    "PostgresError",
    "__version__",
    "__author__",
    "__maintainer__",
    "__license__",
    "__url__",
    "CommandHandler",
    "HOME_CONFIG",
    "DEV_HOME_CONFIG",
    "DEV_LOG_CONFIG",
    "CONFIG_SCHEMA",
    "CleanSchemaT",
    "sqlite",
]
