"""An SQLite3 to PostgreSQL database migration tool."""
import typing

from .cli import *
from .modules import *

__version__ = "0.1.4"
__author__ = "Jonxslays"
__maintainer__ = "Jonxslays"
__license__ = "BSD-3-Clause"
__url__ = "https://github.com/Jonxslays/sqlite2pg"

__all__ = [
    "Worker",
    "Sqlite2pgError",
    "SqliteError",
    "PostgresError",
    "__version__",
    "__author__",
    "__maintainer__",
    "__license__",
    "__url__",
    "CommandHandler",
    "CleanSchemaT",
    "sqlite",
]
