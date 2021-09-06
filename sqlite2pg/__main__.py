import logging

from sqlite2pg import LogConfig
from sqlite2pg import Worker
from sqlite2pg import CommandHandler


def main() -> None:
    """Entry point for the program."""

    handler: CommandHandler = CommandHandler()

    logger = handler.main_cli()

    worker: Worker = Worker(logger)

    # worker.execute()

    logger.debug("cleaned up. exiting...")


if __name__ == "__main__":
    main()
