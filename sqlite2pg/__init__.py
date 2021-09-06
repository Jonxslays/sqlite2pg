"""An Sqlite3 to Postgresql database migration tool."""
import typing


from .config import *
from .errors import *
from .cli import *
from .worker import *


__version__: str = "0.1.1"
__author__: str = "Jonxslays"
__maintainer__: str = "Jonxslays"
__license__: str = "BSD-3-Clause"
__url__: str = "https://github.com/Jonxslays/sqlite2pg"

__all__: typing.List[str] = [
    "Worker",
    "LogConfig",
    "Sqlite2pgError",
    "SqliteError",
    "PostgresError",
    "CommandHandler",
]
