import logging

from sqlite2pg import Logger
from sqlite2pg import Worker


logger: logging.Logger = Logger.new(
    file_path="./test.log",
)


def main():
    """Entry point for the program."""

    logger.debug("sqlite2pg starting...")

    worker = Worker(logger)
    worker.execute()

    logger.debug("cleaned up. exiting...")


if __name__ == "__main__":
    main()
