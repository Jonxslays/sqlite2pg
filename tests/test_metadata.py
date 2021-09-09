import re

from sqlite2pg import __author__, __license__, __maintainer__, __url__, __version__


def test_metadata() -> None:
    with open("pyproject.toml", "r") as f:
        meta = f.read()

        ver = re.findall(r"version = \"(.*)\"", meta)[0]
        author = re.findall(r"authors = \[\"(.*)\"\]", meta)[0]
        license = re.findall(r"license = \"(.*)\"", meta)[0]
        url = re.findall(r"repository = \"(.*)\"", meta)[0]

    assert author == __author__
    assert author == __maintainer__
    assert license == __license__
    assert url == __url__
    assert ver == __version__
