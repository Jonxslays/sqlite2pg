import os
import sqlite3
import time
import typing
from pathlib import Path

from loguru import logger

from sqlite2pg.modules import sqlite

__all__: typing.List[str] = [
    "Worker",
    "CleanSchemaT",
]


# Represents the schema dicts used later on.
RawSchemaT = typing.MutableMapping[str, typing.List[typing.Sequence[str]]]
CleanSchemaT = typing.MutableMapping[str, typing.List[str]]


class Worker:
    """The object that carries the workload of the program.

    Args:
        logger: logging.Logger
            The logger to use for the worker. This logger will be
            supplied automatically by the command line entry point.
    """

    __slots__: typing.Sequence[str] = ("test_sqlite_db",)

    def __init__(self) -> None:
        logger.debug("worker initialized...")
        self.test_sqlite_db: Path = Path("./database.db3")

    def get_sqlite_schema(self, db: Path) -> CleanSchemaT:
        """Gets the schema for a given sqlite3 database.3

        Args:
            db: str
                The path to the sqlite database to get the schema for.

        Returns:
            CleanSchemaT:
                A mapping containing the schema for the tables found
                in the database.
        """

        start: float = time.time()

        # Validate that the database file exists
        if not os.path.isfile(db):
            logger.error(f"can't connect to '{db}', the file doesnt exist.")
            exit(1)

        # Connect to the database, and obtain a cursor.
        logger.debug(f"connecting to: '{db}'.")
        conn: sqlite3.Connection = sqlite3.connect(db)
        cur: sqlite3.Cursor = conn.cursor()

        # Assign 2 mappings for raw and clean schema.
        raw_schema: RawSchemaT = {}
        clean_schema: CleanSchemaT = {}

        try:
            logger.debug("attempting to fetch tables from sqlite master.")

            # Gather all table names
            cur.execute(sqlite.get_tables())

        # We were unable to fetch the data, likely it was not a database.
        except sqlite3.DatabaseError as e:
            logger.debug(f"{e.__class__.__name__}: {e}")
            logger.error(f"'{db}' is not a database. exiting...")
            exit(1)

        else:
            logger.info(f"connection to '{db}' secured.")

        # Iterate through table names.
        for table in [d[0] for d in cur.fetchall()]:
            logger.info(f"fetching schema for '{table}'.")

            # Gather the schema for that table.
            cur.execute(sqlite.get_schema(table))

            # If there is no schema, error.
            data = cur.fetchall()
            if not data:
                logger.error(f"found '{table}' but no schema. exiting...")
                conn.close()
                exit(1)

            # Assign that schema to our schema dict.
            logger.debug(f"found schema for '{table}'.")
            raw_schema[table] = data

        # We didn't find tables or schema.
        if not raw_schema:
            logger.error("no tables found. exiting...")
            conn.close()
            exit(1)

        # Replace tabs with 4 spaces and create
        # a list of strings instead of a list
        # of tuples with one string inside.
        # Add this list to the clean mapping.
        for t, q in raw_schema.items():
            clean_schema[t] = [q[0][0].replace("\t", "    ") + ";"]

        # Close the connection to sqlite
        logger.debug(f"closed connection to sqlite: '{db}'.")
        conn.close()

        end: float = time.time()

        logger.info(
            f"found {len(clean_schema)} tables and schema in {(end - start) * 1000:.4f} ms."
        )

        return clean_schema

    def convert_sqlite_to_pg(self, schema: CleanSchemaT) -> CleanSchemaT:
        """Converts sqlite queries to postres syntax.

        Args:
            schema: CleanSchemaT
                A mutable mapping of tables to table schema.

        Returns:
            CleanSchemaT:
                A mapping containing the schema for the tables from
                sqlite transformed to fit postgres syntax.
        """

        start: float = time.time()
        logger.debug("beginning conversion to postgres syntax")

        # Iterate over each table and alter its schema
        for table, query in schema.items():
            buffer: str = query[0]

            # Postgres doesn't like double quotes.
            buffer = buffer.replace('"', "'")
            # Sqlite integers can be larger than pgsql.
            # Handle upper and lower case.
            buffer = buffer.replace("integer", "bigint")
            buffer = buffer.replace("INTEGER", "BIGINT")

            # Assign the new schema back to the table
            # now the that is has been converted.
            query[0] = buffer
            logger.debug(f"'{table}' has been converted.")

        end: float = time.time()

        return schema

    def validate_input(self, message: str, bad_actor: int = 0) -> str:
        """Validates user confirmation input.

        Args:
            message: str
                The message received from stdin.
            bad_actor: int, optional
                The amount of invalid inputs received thus far.
                Defaults to 0.

        Returns:
            str: The text from the users confirmation
        """

        logger.debug(f"Input validation (attempt {bad_actor + 1}).")
        validated: str = input(message)

        # Handle case where user inputs nothing.
        while not validated or validated[0] not in "yYnN":
            bad_actor += 1

            if bad_actor >= 3:
                logger.error("too many failed inputs. exiting...")
                exit(1)

            validated = self.validate_input(message, bad_actor)

        if validated[0] not in "yY":
            logger.debug(f"user chose to exit with input: '{validated}'.")
            logger.info("exiting...")
            exit(0)

        logger.debug(f"user accepted with input: '{validated}'.")
        return validated

    def execute(self) -> None:
        """Execute the main logic of the program."""

        # Gather the sqlite schema from the database.
        sqlite_schema = self.get_sqlite_schema(self.test_sqlite_db)

        # Validate we gather the correct schema.
        self.validate_input("does the schema look correct [y/n]: ")

        # Validate the converted schema is correct
        converted_schema = self.convert_sqlite_to_pg(sqlite_schema)

        # Validate the converted schema is correct
        self.validate_input("does the converted schema look correct [y/n]: ")

        print("No further logic is implemented.")
        exit(0)

        # TODO
        # Connect to postgres
        # Create the tables
        # Get the actual data from the tables in sqlite
        # Insert the data into postgres
        # Could we use pandas to move the data?
