import typing

__all__: typing.List[str] = [
    "Sqlite2pgError",
    "SqliteError",
    "PostgresError",
    "LoggingConfigError",
]


# Do we need these???
class Sqlite2pgError(Exception):
    """Base Exception that all sqlite2pg exceptions inherit from."""

    __slots__: typing.Sequence[str] = ()
    pass


class SqliteError(Sqlite2pgError):
    """Represents an error in an sqlite3 related action."""

    __slots__: typing.Sequence[str] = ()
    pass


class PostgresError(Sqlite2pgError):
    """Represents an error in an sqlite3 related action."""

    __slots__: typing.Sequence[str] = ()
    pass


class LoggingConfigError(Sqlite2pgError):
    """Represents an error in logging configuration."""

    __slots__: typing.Sequence[str] = ()
    pass
