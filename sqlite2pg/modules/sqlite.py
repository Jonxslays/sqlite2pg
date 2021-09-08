import typing

__all__: typing.List[str] = [
    "get_tables",
    "get_schema",
]


def get_tables() -> str:
    return """
        SELECT name FROM sqlite_master
        WHERE type IS 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY 1
        """


def get_schema(table: str) -> str:
    return f"""
        SELECT sql
        FROM sqlite_master
        WHERE name='{table}'
        """
