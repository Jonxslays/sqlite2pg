import typing
from pathlib import Path

import nox


def install(session: nox.Session, dev: typing.Optional[bool] = False) -> nox.Session:
    session.run("poetry", "shell", external=True)

    if dev:
        session.run("poetry", "install", "-n", external=True)
    else:
        session.run("poetry", "install", "-n", "--no-dev", external=True)

    return session


@nox.session(reuse_venv=True)
def testing(session: nox.Session) -> None:
    session = install(session)
    session.run("pytest", "--verbose")


@nox.session(reuse_venv=True)
def type_checking(session: nox.Session) -> None:
    session = install(session, True)
    session.run("mypy", ".", "--strict")


@nox.session(reuse_venv=True)
def formatting(session: nox.Session) -> None:
    session = install(session, True)
    session.run("black", ".", "-l99")


@nox.session(reuse_venv=True)
def import_checking(session: nox.Session) -> None:
    session = install(session, True)
    session.run(
        "flake8",
        "sqlite2pg",
        "tests",
        "--select",
        "F4",
        "--extend-ignore",
        "E,F",
        "--extend-exclude",
        "__init__.py",
    )
    session.run("isort", ".", "-cq", "--profile", "black")
